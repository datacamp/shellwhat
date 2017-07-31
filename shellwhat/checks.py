import re
from functools import partial

def test_output_contains(state, text, msg = "Submission does not contain the code `{}`.", fixed = False):
    stu_output = state.student_result

    _msg = msg.format(text)

    # either simple text matching or regex test
    res = text in stu_output if fixed else re.search(text, stu_output)

    if not res:
        state.do_test(_msg)

    return state

def test_expr(state, expr,
               msg,
               strict = False,
               output = None,
               test = "output"):
    """Test the result of running shell expression.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        expr : expression to run in the shell.
        msg  : feedback message if expression result is not in output.
        strict: whether result must be exactly equal to output, or (if False) contained therein.
        output: overrides the output that the expression result is compared to.
        test  : whether to use stdout ("output") from the expression, or its exit code ("error")

    """

    stu_output = output if output is not None else state.student_result

    res = state.student_conn.run_command(expr)
    if test == 'error':
        # set res to exit code for prev command
        res = state.student_conn.run_command(" echo $?").rstrip()

    if (strict and res != stu_output) or (res not in stu_output):
        _msg = msg.format(expr, output)
        state.do_test(msg)

    return state

test_expr_output = partial(test_expr,
                           msg = "Could not find the result of `{}` in your output.",
                           test = "output")

test_expr_error = partial(test_expr,
                          msg = "Could not find the exit code `{1}` when running the expression `{0}`.",
                          strict = True,
                          output = "0",
                          test = "error")
