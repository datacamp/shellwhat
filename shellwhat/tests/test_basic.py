from shellwhat.test_exercise import test_exercise as te
from functools import partial

import pytest

@pytest.fixture
def te_sct():
    result = "file1.txt file2.txt"
    return partial(te,
        student_code = "ls -t",
        solution_code = "ls -t",
        pre_exercise_code = "",
        student_conn = None,
        solution_conn = None,
        student_result = result,
        solution_result = None,
        ex_type="NormalExercise",
        error=[]
        )


def test_test_student_typed_pass(te_sct):
    sct_payload = te_sct("Ex().test_student_typed('ls -t', fixed = True)")
    assert sct_payload.get('correct') == True

def test_test_student_typed_fail(te_sct):
    sct_payload = te_sct("Ex().test_student_typed('ls -G', fixed = True)")
    assert sct_payload.get('correct') == False

def test_test_output_contains_pass(te_sct):
    sct_payload = te_sct("Ex().test_output_contains('file1', fixed = True)")
    assert sct_payload.get('correct') == True

def test_test_output_contains_fail(te_sct):
    sct_payload = te_sct("Ex().test_output_contains('ZZZ', fixed = True)")
    assert sct_payload.get('correct') == False
