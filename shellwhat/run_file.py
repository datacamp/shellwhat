import subprocess

from protowhat.Reporter import Reporter


def run(state):
    """Run the student file focused by ``check_file``.

    Args:
        state (State): state as passed by the SCT chain. Don't specify this explicitly.

    :Example:

        Suppose the student has a file ``script.sh`` in ``/home/repl/``::

            echo 'test'

        We can check if the file runs with this SCT::

            Ex().check_file(
                "script.sh"
            ).run()
    """
    student_result, error = run_file(state.path)
    return state.to_child(
        student_result=student_result,
        reporter=Reporter(state.reporter, errors=[error] if error else []),
    )


def run_file(path):
    output, exception = None, None
    try:
        output = subprocess.check_output(["/bin/bash", str(path)], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        exception = (
            "returned non-zero exit status "
            + str(e.returncode)
            + " "
            + str(e.stderr, "utf-8")
        )

    try:
        output = str(output, "utf-8")
    except TypeError:
        pass

    return output, exception
