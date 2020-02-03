import pytest
import os
import subprocess

from pexpect import replwrap
from tempfile import TemporaryDirectory
from pathlib import Path

from protowhat.Reporter import Reporter
from protowhat.failure import TestFail as TF

from shellwhat.checks import has_output
from shellwhat.checks.has_funcs import strip_ansi, has_expr_output
from shellwhat.run_file import run
from shellwhat.State import State


@pytest.fixture
def state():
    return State(
        student_code="some code\x1b[39;49m",
        solution_code="some code",
        pre_exercise_code="",
        student_conn=replwrap.bash(),
        solution_conn=None,
        student_result="stdout stuff",
        solution_result=None,
        reporter=Reporter(),
    )


@pytest.fixture(scope="function")
def tempdir():
    cwd = os.getcwd()
    with TemporaryDirectory() as tmp:
        os.chdir(tmp)
        yield tmp
        os.chdir(cwd)


def test_run_student_code_is_run(state, tempdir):
    # Given
    state.student_code = "touch testfile.sh\n"
    state.solution_code = ""

    filedir = tempdir + "/myscript.sh"
    with open(filedir, "w+") as f:
        f.write("#!/bin/bash\n")
        f.write(state.student_code)

    subprocess.run(["chmod", "+x", filedir])
    state.path = Path(filedir)

    # When
    run(state)

    # Then
    assert os.path.exists(filedir)


def test_run_student_code_output(state, tempdir):
    # Given
    state.student_code = "echo 'test'\n"
    state.solution_code = ""

    filedir = tempdir + "/myscript.sh"
    with open(filedir, "w+") as f:
        f.write("#!/bin/bash\n")
        f.write(state.student_code)

    subprocess.run(["chmod", "+x", filedir])
    state.path = Path(filedir)

    # When
    state = run(state)

    # Then
    assert state.student_result == "test\n"


def test_run_student_code_no_output(state, tempdir):
    # Given
    state.student_code = "ech"
    state.solution_code = "ech"

    filedir = tempdir + "/myscript.sh"
    with open(filedir, "w+") as f:
        f.write("#!/bin/bash\n")
        f.write(state.student_code)

    state.path = Path(filedir)

    # When
    state = run(state)

    # Then
    assert state.student_result is None
    with pytest.raises(TF):
        has_output(state, 'test')
    with pytest.raises(TF):
        has_expr_output(state, output="test")
    strip_ansi(state)


def test_run_student_code_env_var_access(state, tempdir):
    # Given
    os.environ["ENVVARTEST"] = "envtest"
    state.student_code = "echo $ENVVARTEST\n"
    state.solution_code = ""

    filedir = tempdir + "/myscript.sh"
    with open(filedir, "w+") as f:
        f.write("#!/bin/bash\n")
        f.write(state.student_code)

    subprocess.run(["chmod", "+x", filedir])
    state.path = Path(filedir)

    # When
    state = run(state)

    # Then
    assert state.student_result == "envtest\n"


def test_run_student_code_error(state, tempdir):
    # Given
    state.student_code = '>&2 echo "Noooo!"\nexit 5\n'
    state.solution_code = ""

    filedir = tempdir + "/myscript.sh"
    with open(filedir, "w+") as f:
        f.write("#!/bin/bash\n")
        f.write(state.student_code)

    subprocess.run(["chmod", "+x", filedir])
    state.path = Path(filedir)

    # When
    state = run(state)

    # Then
    assert state.reporter.errors == ["returned non-zero exit status 5 Noooo!\n"]
