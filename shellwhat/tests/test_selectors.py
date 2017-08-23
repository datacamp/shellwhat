from shellwhat.State import State
from protowhat.Reporter import Reporter
from protowhat.Test import TestFail as TF
from protowhat.checks.check_funcs import check_node, check_field, has_equal_ast

import pytest
from functools import reduce

def reduce_path(path):
    return reduce(lambda x, y: y(x))

@pytest.fixture('function')
def state():
    return State(student_code = "echo a $b ${c}",
                 solution_code = "echo a $b ${c} unique",
                 pre_exercise_code = "",
                 student_conn = None,
                 solution_conn = None,
                 student_result = "",
                 solution_result = "",
                 reporter = Reporter()
                 )

def test_osh_selector_result(state):
    target = state.ast_dispatcher.nodes.get('CompoundWord')
    cl = check_node(state, "SimpleCommand")
    cmd = check_field(cl, 'words', 0)
    assert isinstance(cmd.student_ast, target)
    assert cmd.student_ast.parts[0].token == "echo"

def test_osh_selector_var_sub(state):
    target = state.ast_dispatcher.nodes.get('SimpleVarSub')
    cl = check_node(state, "SimpleCommand")
    word = check_field(cl, 'words', 2)
    varsub = check_field(word, 'parts', 0)

    assert isinstance(varsub.student_ast, target)
    assert varsub.student_ast.token == "$b"

def test_osh_selector_high_priority(state):
    target = state.ast_dispatcher.nodes.get('BracedVarSub')
    child = check_node(state, 'BracedVarSub', priority = 99)
    assert isinstance(child.student_ast, target)
    assert child.student_ast.token == 'c'

def test_osh_selector_fail(state):
    child = check_node(state, 'SimpleCommand')
    with pytest.raises(TF):
        check_field(child, 'words', 4)

def test_has_equal_ast_simple(state):
    pass
