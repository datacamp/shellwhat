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
               incorrect_msg="The checker expected to find `{{text}}` in the output of your command.",
               fixed = False,
               strip_ansi = True):
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
        _msg = state.build_message(incorrect_msg, fmt_kwargs={ 'text': text })
        state.do_test(_msg)

    return state

def has_expr(state, expr,
              incorrect_msg,
              strict = False,
              output = None,
              test = "output",
              strip_ansi = True):
    stu_output = output if output is not None else state.student_result

    if strip_ansi: stu_output = _strip_ansi(stu_output)

    res = state.student_conn.run_command(expr)
    if test == 'error':
        # set res to exit code for prev command
        res = state.student_conn.run_command(" echo $?").rstrip()

    if (strict and res != stu_output) or (res not in stu_output):
        _msg = state.build_message(incorrect_msg, fmt_kwargs={ 'expr':expr, 'output':output })
        state.do_test(_msg)

    return state


docstr = """Run a shell expression, and see if its result/error is in the output or in manually specified output.

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
    """

has_expr_output = partial(has_expr,
                           incorrect_msg="The checker expected to find the result of `{{expr}}` in your output, but couldn't.",
                           test="output")
has_expr_output.__doc__ = docstr

has_expr_error = partial(has_expr,
                         incorrect_msg="The checker expected to get the error code `{{output}}` when executing `{{expr}}` in your output, but didn't.",
                         strict=True,
                         test="error")
has_expr_error.__doc__ = docstr