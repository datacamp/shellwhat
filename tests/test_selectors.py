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

@pytest.fixture('function')
def d():
    return State.get_dispatcher()

@pytest.mark.osh
class TestOsh:
    def test_osh_dispatcher_ast_fails_hard(self, d):
        with pytest.raises(d.ParseError): d.ast.parse("for ii")

    def test_osh_dispatcher_fails_gracefully(self, d):
        d.parse("for ii")

    def test_osh_selector_result(self, state):
        target = state.ast_dispatcher.nodes.get('CompoundWord')
        cl = check_node(state, "SimpleCommand")
        cmd = check_field(cl, 'words', 0)
        assert isinstance(cmd.student_ast, target)
        assert cmd.student_ast.parts[0].token == "echo"

    def test_osh_selector_var_sub(self, state):
        target = state.ast_dispatcher.nodes.get('SimpleVarSub')
        cl = check_node(state, "SimpleCommand")
        word = check_field(cl, 'words', 2)
        varsub = check_field(word, 'parts', 0)

        assert isinstance(varsub.student_ast, target)
        assert varsub.student_ast.token == "$b"

    def test_osh_selector_high_priority(self, state):
        target = state.ast_dispatcher.nodes.get('BracedVarSub')
        child = check_node(state, 'BracedVarSub', priority = 99)
        assert isinstance(child.student_ast, target)
        assert child.student_ast.token == 'c'

    def test_osh_selector_fail(self, state):
        child = check_node(state, 'SimpleCommand')
        with pytest.raises(TF):
            check_field(child, 'words', 4)

    def test_osh_transformer_omits_sentence(self):
        d = State.get_dispatcher()
        tree = d.parse("echo a b c;")
        assert isinstance(tree.children[0], d.nodes.get('SimpleCommand'))

    def test_has_equal_ast_simple(self, state):
        state.solution_ast = state.ast_dispatcher.ast.parse("echo a $b ${c}")
        has_equal_ast(state)

    def test_has_equal_ast_simple_fail(self, state):
        with pytest.raises(TF):
            has_equal_ast(state)

    def test_has_equal_ast_subcode(self, state):
        word = check_field(check_node(state, 'SimpleCommand'), 'words', 0)
        has_equal_ast(word)

    @pytest.mark.xfail #TODO: speaker for osh ast
    def test_dispatcher_ast_path(self):
        d = State.get_dispatcher()
        node = d.parse("echo a b c")
        assert d.describe(node) == "command list"    # note: for CommandList node
