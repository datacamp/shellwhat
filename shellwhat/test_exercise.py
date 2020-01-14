from protowhat.failure import Failure, InstructorError
from protowhat.Reporter import Reporter

from shellwhat.sct_syntax import SCT_CTX
from shellwhat.State import State


def test_exercise(
    sct,
    student_code,
    student_result,
    student_conn,
    solution_code,
    solution_result,
    solution_conn,
    pre_exercise_code,
    ex_type,
    error,
    force_diagnose=False,
    debug=False,  # currently unused
):
    """
    """

    reporter = Reporter(errors=error)

    state = State(
        student_code=student_code,
        solution_code=solution_code,
        pre_exercise_code=pre_exercise_code,
        student_conn=student_conn,
        solution_conn=solution_conn,
        student_result=student_result,
        solution_result=solution_result,
        reporter=reporter,
        force_diagnose=force_diagnose,
    )

    State.root_state = state
    SCT_CTX["Ex"].root_state = state

    def add_student_code(data):
        data["student_code"] = student_code
        return data

    try:
        exec(sct, SCT_CTX)
    except Failure as e:
        if isinstance(e, InstructorError):
            # TODO: decide based on context
            raise e
        return add_student_code(reporter.build_failed_payload(e.feedback))

    return add_student_code(reporter.build_final_payload())
