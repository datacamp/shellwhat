from shellwhat.State import State
from shellwhat.checks.check_funcs import strip_ansi, has_code, has_expr_output, has_expr_error
from protowhat.checks.check_logic import multi
from protowhat.Reporter import Reporter
from protowhat.Test import TestFail as TF
from pexpect import replwrap

import pytest

@pytest.fixture
def state():
    return State(student_code = "some code\x1b[39;49m",
                 solution_code = "some code",
                 pre_exercise_code = "",
                 student_conn = replwrap.bash(),
                 solution_conn = None,
                 student_result = "stdout stuff",
                 solution_result = None,
                 reporter = Reporter())

def test_strip_ansi(state):
    state.student_result = 'file1.txt \x1b[39;49m\x1b[0mfile2.txt'
    assert strip_ansi(state).student_result == 'file1.txt file2.txt'

def test_has_expr_output(state):
    has_expr_output(state, "echo -n stdout stuff")

def test_has_expr_output_fail(state):
    with pytest.raises(TF):
        has_expr_output(state, "echo stdout stuff")

def test_has_expr_output_strict_true_fail(state):
    with pytest.raises(TF):
        has_expr_output(state, "echo -n stdout", strict = True)

def test_has_expr_error(state):
    has_expr_error(state, "echo -n stdout stuff", output = "0")

def test_has_expr_error_fail(state):
    with pytest.raises(TF):
        has_expr_error(state, "ls filethatdoesnotexist.txt")

def test_has_expr_error_code1(state):
    # cat is used here since BSD and GNU ls use different exit_codes
    has_expr_error(state, "cat filethatdoesnotexist.txt", output = "1")

def test_has_expr_error_code1_fail(state):
    with pytest.raises(TF):
        has_expr_error(state, "ls", output = "1")

# ensure protowhat SCTs work --------------------------------------------------

def test_multi(state):
    multi(state, lambda s: has_code(s, "some code"))

def test_multi_fail(state):
    with pytest.raises(TF):
        multi(state, lambda s: has_code(s, "some code abc"))
