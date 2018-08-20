from shellwhat.State import State
from shellwhat.checks.check_funcs import strip_ansi, has_code, has_expr_output, has_expr_error
from protowhat.checks.check_logic import multi
from protowhat.Reporter import Reporter
from protowhat.Test import TestFail as TF
from pexpect import replwrap

import pytest

def prepare_state(stu_code, sol_code):
    return State(
        student_code = stu_code,
        solution_code = sol_code,
        reporter = Reporter(),
        # args below should be ignored
        pre_exercise_code = "NA",
        student_result = 'stu_result',
        solution_result = None,
        student_conn = replwrap.bash(),
        solution_conn = None)

def test_has_code():
    state = prepare_state('b', 'b')
    with pytest.raises(TF, match = 'The checker expected to find `not_in_code`'):
        has_code(state, 'not_in_code')

def test_has_output():
    pass

def test_has_expr_output():
    pass

def test_has_expr_error():
    pass