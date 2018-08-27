import re
from functools import partial

ANSI_REGEX = r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]"

def _strip_ansi(result):
    return re.sub(ANSI_REGEX, '', result)

def strip_ansi(state):
    """Remove ANSI escape codes from student result."""
    stu_res = _strip_ansi(state.student_result)

    return state.to_child(student_result = stu_res)

def has_code(state, text, incorrect_msg="The checker expected to find `{{text}}` in your command.", fixed=False):
    """Check whether the student code contains text.

    This function is a simpler override of the `has_code` function in protowhat,
    because ``ast_node._get_text()`` is not implemented in the OSH parser

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

    stu_code = state.student_code

    # either simple text matching or regex test
    res = text in stu_code if fixed else re.search(text, stu_code)

    if not res:
        _msg = state.build_message(incorrect_msg, fmt_kwargs={ 'text': text })
        state.do_test(_msg)

    return state

def has_output(state,
               text,
               incorrect_msg="The checker expected to find {{'' if fixed else 'the pattern '}}`{{text}}` in the output of your command.",
               fixed=False,
               strip_ansi=True):
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

    stu_output = state.student_result

    if strip_ansi: stu_output = _strip_ansi(stu_output)

    # either simple text matching or regex test
    res = text in stu_output if fixed else re.search(text, stu_output)

    if not res:
        _msg = state.build_message(incorrect_msg, fmt_kwargs={ 'text': text, 'fixed': fixed })
        state.do_test(_msg)

    return state

def has_cwd(state, dir, incorrect_msg="Your current working directory should be `{{dir}}`. Use `cd {{dir}}` to navigate there."):
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
    _msg = state.build_message(incorrect_msg, fmt_kwargs={ 'dir': dir })
    has_expr_exit_code(state, expr, output="0", incorrect_msg=_msg)
    return state

def has_expr(state,
             expr=None,
             incorrect_msg=None,
             strict=False,
             output=None,
             test="output",
             strip_ansi=True):
    if expr is None: expr = state.solution_code.strip()
    if incorrect_msg is None: raise ValueError("Make sure to specify an incorrect_msg in has_expr")

    # get the output produced by the student
    stu_output = output if output is not None else state.student_result
    if strip_ansi: stu_output = _strip_ansi(stu_output).strip()

    # run the expression
    res = state.student_conn.run_command(expr).strip()
    if strip_ansi: res = _strip_ansi(res).strip()
    if test == 'exit_code':
        # set res to exit code for prev command
        res = state.student_conn.run_command(" echo $?").strip()

    # do the comparison
    if (strict and res != stu_output) or (res not in stu_output):
        _msg = state.build_message(incorrect_msg, fmt_kwargs={ 'expr':expr, 'output':output })
        state.do_test(_msg)

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

example =  """
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

has_expr_output = partial(has_expr,
                           incorrect_msg="The checker expected to find the result of `{{expr}}` in your output, but couldn't.",
                           test="output")
has_expr_output.__doc__ = docstr.format("result") + example

has_expr_exit_code = partial(has_expr,
                         incorrect_msg="The checker expected to get the exit code `{{output}}` when executing `{{expr}}` in your output, but didn't.",
                         strict=True,
                         test="exit_code")
has_expr_exit_code.__doc__ = docstr.format("exit code")