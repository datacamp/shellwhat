def test_output_contains(state, text, msg = "Submission does not contain the code `{}`.", fixed = False):
    stu_output = state.student_result

    _msg = msg.format(text)

    # either simple text matching or regex test
    res = text in stu_output if fixed else re.search(text, stu_output)

    if not res:
        state.do_test(_msg)

    return state
