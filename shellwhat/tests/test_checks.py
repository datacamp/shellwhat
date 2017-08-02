from shellwhat.test_exercise import test_exercise as te
from shellwhat.State import State
from shellwhat import checks
from protowhat.Reporter import Reporter
from protowhat.Test import TestFail as TF
from functools import partial
from pexpect import replwrap

import pytest

@pytest.fixture
def state():
    return State(student_code = "some code", solution_code = "some code",
                 pre_exercise_code = "",
                 student_conn = replwrap.bash(),
                 solution_conn = None,
                 student_result = "stdout stuff",
                 solution_result = None,
                 reporter = Reporter())
                 
def test_expr_output(state):
    checks.test_expr_output(state, "echo -n stdout stuff")

def test_expr_output_fail(state):
    with pytest.raises(TF):
        checks.test_expr_output(state, "echo stdout stuff")

def test_expr_output_strict_true_fail(state):
    with pytest.raises(TF):
        checks.test_expr_output(state, "echo -n stdout", strict = True)

def test_expr_error(state):
    checks.test_expr_error(state, "echo -n stdout stuff")

def test_expr_error_fail(state):
    with pytest.raises(TF):
        checks.test_expr_error(state, "ls filethatdoesnotexist.txt")

def test_expr_error_code1(state):
    # cat is used here since BSD and GNU ls use different exit_codes
    checks.test_expr_error(state, "cat filethatdoesnotexist.txt", output = "1")

def test_expr_error_code1_fail(state):
    with pytest.raises(TF):
        checks.test_expr_error(state, "ls", output = "1")

# ensure protowhat SCTs work --------------------------------------------------

def test_multi(state):
    checks.multi(state, lambda s: checks.test_student_typed(s, "some code"))

def test_multi_fail(state):
    with pytest.raises(TF):
        checks.multi(state, lambda s: checks.test_student_typed(s, "some code abc"))
