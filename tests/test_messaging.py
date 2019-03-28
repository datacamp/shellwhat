from shellwhat.State import State
from shellwhat.checks.has_funcs import *
from protowhat.checks.check_logic import multi
from protowhat.Reporter import Reporter
from protowhat.Test import TestFail as TF
from pexpect import replwrap

import pytest


@pytest.fixture
def state():
    return State(
        student_code="student_code",
        solution_code="solution_code",
        reporter=Reporter(),
        # args below should be ignored
        pre_exercise_code="NA",
        student_result="stu_result",
        solution_result=None,
        student_conn=replwrap.bash(),
        solution_conn=None,
    )


def test_has_code(state):
    with pytest.raises(
        TF, match="The checker expected to find `not_in_code` in your command."
    ):
        has_code(state, "not_in_code")


@pytest.mark.parametrize(
    "fixed, patt",
    [
        (
            True,
            "The checker expected to find `not_in_result` in the output of your command.",
        ),
        (
            False,
            "The checker expected to find the pattern `not_in_result` in the output of your command.",
        ),
    ],
)
def test_has_output(state, fixed, patt):
    with pytest.raises(TF, match=patt):
        has_output(state, "not_in_result", fixed=fixed)


def test_has_cwd(state):
    with pytest.raises(
        TF,
        match="Your current working directory should be `not_right_dir`. Use `cd not_right_dir` to navigate there.",
    ):
        has_cwd(state, "not_right_dir")


def test_has_expr_output():
    pass


def test_has_expr_exit_code():
    pass
