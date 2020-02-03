import re
from functools import partial
from typing import Union

from protowhat.Feedback import FeedbackComponent

from shellwhat.State import State

ANSI_REGEX = r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]"


def _strip_ansi(output: str) -> str:
    if not isinstance(output, str):
        return output
    return re.sub(ANSI_REGEX, "", output)


def strip_ansi(state: State) -> State:
    """Remove ANSI escape codes from student result."""
    return state.to_child(student_result=_strip_ansi(state.student_result))


def has_code(
    state: State,
    text: str,
    incorrect_msg: str = "The checker expected to find `{{text}}` in your command.",
    fixed: bool = False,
) -> State:
    """Check whether the student code contains text.

    This function is a simpler override of the `has_code` function in protowhat,
    because ``ast_node.get_text()`` is not implemented in the OSH parser

    Using ``has_code()`` should be a last resort. It is always better to look at the result of code
    or the side effects they had on the state of your program.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        text : text that student code must contain. Can be a regex pattern or a simple string.
        incorrect_msg: if specified, this overrides the automatically generated feedback message
                       in case ``text`` is not found in the student code.
        fixed: whether to match ``text`` exactly, rather than using regular expressions.

    :Example:

        Suppose the solution requires you to do: ::

            git push origin master

        The following SCT can be written: ::

            Ex().has_code(r'git\\s+push\\s+origin\\s+master')

        Submissions that would pass: ::

            git push origin master
            git   push    origin    master

        Submissions that would fail: ::

            git push --force origin master
    """

    student_code = state.student_code

    # either simple text matching or regex test
    correct = text in student_code if fixed else re.search(text, student_code)

    if not correct:
        state.report(incorrect_msg, {"text": text})

    return state


def has_output(
    state: State,
    text: str,
    incorrect_msg: str = "The checker expected to find {{'' if fixed else 'the pattern '}}`{{text}}` in the output of your command.",
    fixed: bool = False,
    strip_ansi: bool = True,
) -> State:
    """Check whether student output contains specific text.

    Before you use ``has_output()``, have a look at ``has_expr_output()`` or ``has_expr_error()``;
    they might be more fit for your use case.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with ``Ex()``.
        text : text that student output must contain. Can be a regex pattern or a simple string.
        incorrect_msg: if specified, this overrides the automatically generated feedback message
                       in case ``text`` is not found in the student output.
        fixed: whether to match ``text`` exactly, rather than using regular expressions.
        strip_ansi: whether to remove ANSI escape codes from output

    :Example:

        Suppose the solution requires you to do: ::

            echo 'this is a printout!'

        The following SCT can be written: ::

            Ex().has_output(r'this\\s+is\\s+a\\s+print\\s*out')

        Submissions that would pass: ::

            echo 'this   is a print out'
            test='this is a printout!' && echo $test

        Submissions that would fail: ::

            echo 'this is a wrong printout'
    """
    student_output = state.student_result

    if strip_ansi:
        student_output = _strip_ansi(student_output)

    if student_output is None:
        # The output can be None, when using run()
        correct = student_output is text
    else:
        # either simple text matching or regex test
        correct = text in student_output if fixed else re.search(text, student_output)

    if not correct:
        state.report(incorrect_msg, {"text": text, "fixed": fixed})

    return state


def has_cwd(
    state: State,
    dir: str,
    incorrect_msg: str = "Your current working directory should be `{{dir}}`. Use `cd {{dir}}` to navigate there.",
) -> State:
    """Check whether the student is in the expected directory.

    This check is typically used before using ``has_expr_output()``
    to make sure the student didn't navigate somewhere else.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with ``Ex()``.
        dir: Directory that the student should be in. Always use the absolute path.
        incorrect_msg: If specified, this overrides the automatically generated message in
                       case the student is not in the expected directory.

    :Example:

        If you want to be sure that the student is in ``/home/repl/my_dir``: ::

            Ex().has_cwd('/home/repl/my_dir')

    """
    expr = "[[ $PWD == '{}' ]]".format(dir)
    _msg = FeedbackComponent(incorrect_msg, {"dir": dir})
    has_expr_exit_code(state, expr, output="0", incorrect_msg=_msg)
    return state


def has_expr(
    state: State,
    expr: str = None,
    incorrect_msg: Union[str, FeedbackComponent] = None,
    strict: bool = False,
    output: str = None,
    test=str,
    strip_ansi: bool = True,
) -> State:
    if incorrect_msg is None:
        raise ValueError("Make sure to specify an incorrect_msg in has_expr")

    # get the output produced by the student
    full_output = state.student_result if output is None else output
    if strip_ansi:
        full_output = _strip_ansi(full_output)
        if isinstance(full_output, str):
            full_output = full_output.strip()

    # run the expression
    if expr is None:
        expr = state.solution_code.strip()
    expression_output = state.student_conn.run_command(expr).strip()
    if strip_ansi:
        expression_output = _strip_ansi(expression_output).strip()
    if test == "exit_code":
        # set expression_output to exit code for prev command
        expression_output = state.student_conn.run_command(" echo $?").strip()

    # do the comparison
    if (
        (full_output is None and expression_output is not None)
        or (strict and expression_output != full_output)
        or (expression_output not in full_output)
    ):
        if isinstance(incorrect_msg, FeedbackComponent):
            # used by e.g. has_cwd
            state.report(
                incorrect_msg.message,
                {"expr": expr, "output": output, **incorrect_msg.kwargs},
            )
        else:
            state.report(incorrect_msg, {"expr": expr, "output": output})

    return state


docstr = """Run a shell expression, and see if its {} is in the output or in manually specified output.

    By default, the result of the student's code is compared to the result of running ``expr``.
    You can compare the result of running ``expr`` with an arbitrary output by specifing ``output``.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        expr : expression to run in the shell. If not specified, this defaults to the solution code.
        msg  : feedback message if expression result is not in output.
        strict: whether result must be exactly equal to output, or (if False) contained therein.
        output: overrides the output that the expression result is compared to.
        test  : whether to use stdout ("output") from the expression, or its exit code ("error").
        strip_ansi: whether to remove ANSI escape codes from result.
    """

example = """
    :Example:

        As a first example, suppose you expect the student to show the status of a git repository: ::

            git status

        The following SCT would check that: ::

            Ex().has_expr_output()  # expr set to solution code

        As a second example, suppose you want to verify that a student staged
        a the changes to the file `test.txt` in a git repo: ::

            git add test.txt

        The following SCT would check that this file is actually staged: ::

            Ex().has_expr_output(expr="git diff --name-only --staged | grep test.txt",
                                 output="test.txt", strict=True,
                                 incorrect_msg="meaningful message")

        Notice how manually specifying ``expr`` and ``output`` allows you to probe virtually
        any property or state of your terminal without the student knowing.
    """

has_expr_output = partial(
    has_expr,
    incorrect_msg="The checker expected to find the result of `{{expr}}` in your output, but couldn't.",
    test="output",
)
has_expr_output.__name__ = "has_expr_output"
has_expr_output.__doc__ = docstr.format("result") + example

has_expr_exit_code = partial(
    has_expr,
    incorrect_msg="The checker expected to get the exit code `{{output}}` when executing `{{expr}}` in your output, but didn't.",
    strict=True,
    test="exit_code",
)
has_expr_exit_code.__name__ = "has_expr_exit_code"
has_expr_exit_code.__doc__ = docstr.format("exit code")
