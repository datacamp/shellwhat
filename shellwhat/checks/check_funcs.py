import re
from functools import partial

ANSI_REGEX = r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]"

def _strip_ansi(result):
    return re.sub(ANSI_REGEX, '', result)

def strip_ansi(state):
    """Remove ANSI escape codes from student result"""
    stu_res = _strip_ansi(state.student_result)

    return state.to_child(student_result = stu_res)

def has_code(state, text, incorrect_msg="The checker expected to find `{{text}}` in your command.", fixed=False):
    """Override of has_code in protowhat (because ast_node._get_text() is not implemented in OSH parser)"""
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
    """Test whether student output contains specific text.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        text : text that student output must contain.
        msg  : feedback message if text is not in student output.
        fixed: whether to match text exactly, rather than using regular expressions.
        strip_ansi: whether to remove ANSI escape codes from output

    :Example:

        TODO
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
    """Test whether the user is in the expected directory. This wraps a
    rather inelegant shell expression, which we have to use because os.getcwd()
    returns the directory the evaluator is running in, not the directory the
    user has gone to in the shell.
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
        expr : expression to run in the shell.
        msg  : feedback message if expression result is not in output.
        strict: whether result must be exactly equal to output, or (if False) contained therein.
        output: overrides the output that the expression result is compared to.
        test  : whether to use stdout ("output") from the expression, or its exit code ("error").
        strip_ansi: whether to remove ANSI escape codes from result.

    :Example:

        TODO
    """

has_expr_output = partial(has_expr,
                           incorrect_msg="The checker expected to find the result of `{{expr}}` in your output, but couldn't.",
                           test="output")
has_expr_output.__doc__ = docstr.format("result")

has_expr_exit_code = partial(has_expr,
                         incorrect_msg="The checker expected to get the exit code `{{output}}` when executing `{{expr}}` in your output, but didn't.",
                         strict=True,
                         test="exit_code")
has_expr_exit_code.__doc__ = docstr.format("exit code")