import re
from functools import partial, wraps
from protowhat.checks.check_logic import *
from protowhat.checks.check_simple import *
from protowhat.checks.check_funcs import *
from protowhat.checks.check_files import *

ANSI_REGEX = "(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]"

def _strip_ansi(result):
    return re.sub(ANSI_REGEX, '', result)

def strip_ansi(state):
    """Remove ANSI escape codes from student result"""
    stu_res = _strip_ansi(state.student_result)

    return state.to_child(student_result = stu_res)

# TODO: Note that test_student_typed exists in protowhat, but is overwritten below.
#       This is because it uses ast_node._get_text(), which is not implemented in the
#       adaptation of the OSH parser yet (but it could be).
def test_student_typed(state, text, msg="Submission does not contain the code `{}`.", fixed=False):
    """Test whether the student code contains text.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        text : text that student code must contain.
        msg  : feedback message if text is not in student code.
        fixed: whether to match text exactly, rather than using regular expressions.

    :Example:
        If the student code is.. ::

            SELECT a FROM b WHERE id < 100

        Then the first test below would (unfortunately) pass, but the second would fail..::

            # contained in student code
            Ex().test_student_typed(text="id < 10")

            # the $ means that you are matching the end of a line
            Ex().test_student_typed(text="id < 10$")

        By setting ``fixed = True``, you can search for fixed strings::

            # without fixed = True, '*' matches any character
            Ex().test_student_typed(text="SELECT * FROM b")               # passes
            Ex().test_student_typed(text="SELECT \\\\* FROM b")             # fails
            Ex().test_student_typed(text="SELECT * FROM b", fixed=True)   # fails

    """
    stu_ast = state.student_ast
    stu_code = state.student_code

    _msg = msg.format(text)

    # either simple text matching or regex test
    res = text in stu_code if fixed else re.search(text, stu_code)

    if not res:
        state.do_test(_msg)

    return state

def test_output_contains(state,
                         text,
                         msg = "Submission does not contain the code `{}`.",
                         fixed = False,
                         strip_ansi = True):
    """Test whether student output contains specific text.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        text : text that student output must contain.
        msg  : feedback message if text is not in student output.
        fixed: whether to match text exactly, rather than using regular expressions.
        strip_ansi: whether to remove ANSI escape codes from output

    """

    stu_output = state.student_result

    if strip_ansi: stu_output = _strip_ansi(stu_output)

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
              test = "output",
              strip_ansi = True):
    """Test the result of running shell expression.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        expr : expression to run in the shell.
        msg  : feedback message if expression result is not in output.
        strict: whether result must be exactly equal to output, or (if False) contained therein.
        output: overrides the output that the expression result is compared to.
        test  : whether to use stdout ("output") from the expression, or its exit code ("error").
        strip_ansi: whether to remove ANSI escape codes from result.

    Note:
        The convenience Functions ``test_expr_output`` and ``test_expr_error`` wrap ``test_expr``.

    """

    stu_output = output if output is not None else state.student_result

    if strip_ansi: stu_output = _strip_ansi(stu_output)

    res = state.student_conn.run_command(expr)
    if test == 'error':
        # set res to exit code for prev command
        res = state.student_conn.run_command(" echo $?").rstrip()

    if (strict and res != stu_output) or (res not in stu_output):
        _msg = msg.format(expr, output)
        state.do_test(_msg)

    return state

test_expr_output = partial(test_expr,
                           msg = "Could not find the result of `{}` in your output.",
                           test = "output")

test_expr_error = partial(test_expr,
                          msg = "Could not find the exit code `{1}` when running the expression `{0}`.",
                          strict = True,
                          output = "0",
                          test = "error")
