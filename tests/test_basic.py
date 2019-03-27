from shellwhat.test_exercise import test_exercise as te
from functools import partial

import pytest


@pytest.fixture
def te_sct():
    result = "file1.txt file2.txt"
    return partial(
        te,
        student_code="ls -t",
        solution_code="ls -t",
        pre_exercise_code="",
        student_conn=None,
        solution_conn=None,
        student_result=result,
        solution_result=None,
        ex_type="NormalExercise",
        error=[],
    )


@pytest.mark.parametrize(
    "code,is_correct",
    [
        ("Ex().has_code('ls -t', fixed = True)", True),
        ("Ex().has_code('ls -G', fixed = True)", False),
        ("Ex().has_code('ls -G', fixed = True)", False),
        ("Ex().has_output('file1', fixed = True)", True),
        ("Ex().has_output('ZZZ', fixed = True)", False),
    ],
)
def test_sct(te_sct, code, is_correct):
    sct_payload = te_sct(code)
    assert sct_payload.get("correct") == is_correct
    assert sct_payload.get("student_code") == "ls -t"


def test_sct_check_file():
    sct_payload = te(
        "Ex().check_file('file1.sh', use_fs=False).has_code('hey')",
        student_code={"file1.sh": "echo hey"},
        solution_code={"file1.sh": "echo ya"},
        pre_exercise_code="",
        student_conn=None,
        solution_conn=None,
        student_result="",
        solution_result="",
        ex_type="NormalExercise",
        error=[],
    )
    assert sct_payload.get("correct")
