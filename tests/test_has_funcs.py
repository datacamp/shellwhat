from shellwhat.State import State
from shellwhat.checks.has_funcs import *
from protowhat.checks.check_logic import multi
from protowhat.Reporter import Reporter
from protowhat.Test import TestFail as TF
from pexpect import replwrap

import pytest


@pytest.fixture
def state():
    state = State(
        student_code="some code\x1b[39;49m",
        solution_code="some code",
        pre_exercise_code="",
        student_conn=replwrap.bash(),
        solution_conn=None,
        student_result="stdout stuff",
        solution_result=None,
        reporter=Reporter(),
    )
    state.root_state = state
    return state


def test_strip_ansi(state):
    state.student_result = "file1.txt \x1b[39;49m\x1b[0mfile2.txt"
    assert strip_ansi(state).student_result == "file1.txt file2.txt"


def test_has_cwd(state):
    cwd = state.student_conn.run_command("pwd").strip()
    has_cwd(state, cwd)
    state.student_conn.run_command("cd ~")
    with pytest.raises(TF):
        has_cwd(state, cwd)


# has_expr ---------------------------------------------------------------


def test_has_expr_output_pass(state):
    state.solution_code = "echo 'stdout stuff'"
    has_expr_output(state)


@pytest.mark.parametrize(
    "expr, strict",
    [
        ("echo stdout stuff", False),
        ("echo 'stdout stuff\n'", False),
        ("echo '\nstdout stuff\n'", False),
        ("echo '\nstdout stuff\n'", False),
        ("echo stdout stuff", True),
        ("echo 'stdout stuff\n'", True),
        ("echo '\nstdout stuff\n'", True),
        ("echo '\nstdout stuff\n'", True),
    ],
)
def test_has_expr_output_pass_2(state, expr, strict):
    has_expr_output(state, expr, strict=strict)


@pytest.mark.parametrize(
    "expr, strict", [("echo wrong stuff", False), ("echo stdout", True)]
)
def test_has_expr_output_fail(state, expr, strict):
    with pytest.raises(TF):
        has_expr_output(state, expr, strict=strict)


def test_has_expr_exit_code(state):
    has_expr_exit_code(state, "echo -n stdout stuff", output="0")


def test_has_expr_exit_code_fail(state):
    with pytest.raises(TF):
        has_expr_exit_code(state, "ls filethatdoesnotexist.txt")


def test_has_expr_exit_code_code1(state):
    # cat is used here since BSD and GNU ls use different exit_codes
    has_expr_exit_code(state, "cat filethatdoesnotexist.txt", output="1")


def test_has_expr_exit_code_code1_fail(state):
    with pytest.raises(TF):
        has_expr_exit_code(state, "ls", output="1")


# ensure protowhat SCTs work --------------------------------------------------


def test_multi(state):
    multi(state, lambda s: has_code(s, "some code"))


def test_multi_fail(state):
    with pytest.raises(TF):
        multi(state, lambda s: has_code(s, "some code abc"))
