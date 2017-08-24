from protowhat.selectors import Dispatcher
from protowhat.State import State as BaseState

from protowhat.utils_ast import AstModule
from ast import NodeTransformer


from subprocess import check_output
import shlex
import json

PARSER_OSH_STUB = ["python2", "-m", "osh"]
#PARSER_OSH_STUB = ["docker", "exec", "oilc", "python2", "-m", "osh"]


class OshTransformer(NodeTransformer):
    """Does some reshaping on tree. For example, dropping or modifying nodes"""

    def visit_Sentence(self, node):
        return node.child

class OshParser(AstModule):
    def parse(self, code, strict = True):
        res = check_output(PARSER_OSH_STUB + [code])
        ast_dict = json.loads(res.decode())
        tree = self.load(ast_dict)
        return OshTransformer().visit(tree)


class State(BaseState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_dispatcher():
        ast_mod = OshParser()
        return Dispatcher(ast_mod.classes, ast_mod)
        
