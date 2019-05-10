import pytest

from shellwhat.State import State
from shellwhat.reporter import Reporter
from protowhat.Test import TestFail as TF
from protowhat.checks.check_funcs import check_node, check_edge, has_equal_ast
from shellwhat.parsers import OshParser


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    OshParser.nodes = {}


@pytest.fixture("function")
def state():
    state = State(
        student_code="echo a $b ${c}",
        solution_code="echo a $b ${c} unique",
        pre_exercise_code="",
        student_conn=None,
        solution_conn=None,
        student_result="",
        solution_result="",
        reporter=Reporter(),
    )
    state.root_state = state
    return state


@pytest.fixture("function")
def d():
    return state().get_dispatcher()


@pytest.fixture("function")
def shell_script():
    return """# Use curl, download file from URL and rename
curl -o Spotify201812.zip -L https://tinyurl.com/Zipped201812Spotify

# Unzip file then delete original zipped file
unzip Spotify201812.zip && rm Spotify201812.zip

# View url_list.txt to verify content
cat url_list.txt

# Use wget, download all files in url_list.txt
wget -i url_list.txt

# Take a look at all files downloaded
ls"""


@pytest.mark.osh
class TestOsh:
    # TODO: check top node?
    def test_osh_parsing(self, d, shell_script):
        d.ast_mod.parse(shell_script)

    def test_sct(self, shell_script):
        from shellwhat.test_exercise import test_exercise as te

        sct_payload = te(
            """
Ex().check_node('SimpleCommand', 0).multi(
  check_edge('words', 0).has_equal_ast(),
  check_edge('words', 1).has_equal_ast(),
  check_edge('words', 2).has_equal_ast(),
  check_edge('words', 3).has_equal_ast(),
  check_edge('words', 4).has_equal_ast()
)""",
            student_code=shell_script,
            solution_code=shell_script,
            pre_exercise_code="""from urllib.request import urlretrieve
url = 'https://assets.datacamp.com/production/repositories/4180/datasets/b4e48732f25e87864f6ce23066b8c0d14c7c6430/Chp1Capstone_urlList.txt'
urlretrieve(url, 'url_list.txt')""",
            student_conn=None,
            solution_conn=None,
            student_result="",
            solution_result="",
            ex_type="NormalExercise",
            error=[],
        )
        assert sct_payload.get("correct")

    def test_osh_dispatcher_ast_fails_hard(self, d):
        with pytest.raises(d.ParseError):
            d.ast_mod.parse("for ii")

    def test_osh_dispatcher_fails_gracefully(self, d):
        d.parse("for ii")

    def test_osh_selector_result(self, state):
        target = state.ast_dispatcher.nodes.get("CompoundWord")
        cmd = check_edge(state, "words", 0)
        assert isinstance(cmd.student_ast, target)
        assert cmd.student_ast.parts[0].token.val == "echo"

    def test_osh_selector_var_sub(self, state):
        target = state.ast_dispatcher.nodes.get("SimpleVarSub")
        word = check_edge(state, "words", 2)
        varsub = check_edge(word, "parts", 0)

        assert isinstance(varsub.student_ast, target)
        assert varsub.student_ast.token.val == "$b"

    def test_osh_selector_high_priority(self, state):
        target = state.ast_dispatcher.nodes.get("BracedVarSub")
        child = check_node(state, "BracedVarSub", priority=99)
        assert isinstance(child.student_ast, target)
        assert child.student_ast.token.val == "c"
        with pytest.raises(TF):
            child.report("test")

    def test_osh_selector_fail(self, state):
        with pytest.raises(TF):
            check_edge(state, "words", 4)

    def test_osh_transformer_omits_sentence(self, d):
        tree = d.parse("echo a b c;")
        assert isinstance(tree.child, d.nodes.get("SimpleCommand"))

    def test_has_equal_ast_simple(self, state):
        state.solution_ast = state.ast_dispatcher.ast_mod.parse("echo a $b ${c}")
        has_equal_ast(state)

    def test_has_equal_ast_simple_fail(self, state):
        with pytest.raises(TF):
            has_equal_ast(state)

    def test_has_equal_ast_subcode(self, state):
        word = check_edge(state, "words", 0)
        has_equal_ast(word)

    @pytest.mark.xfail  # TODO: speaker for osh ast
    def test_dispatcher_ast_path(self, d):
        node = d.parse("echo a b c")
        assert d.describe(node) == "command list"  # note: for CommandList node
