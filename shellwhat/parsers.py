from protowhat.utils_ast import AstModule
from ast import NodeTransformer
from subprocess import check_output
import json

#PARSER_OSH_STUB = ["docker", "exec", "oilc", "python2", "-m", "osh"]
PARSER_OSH_STUB = ["python2", "-m", "osh"]

class ParseError(Exception): pass

class OshParser(AstModule):
    def parse(self, code, strict = True):
        res = check_output(PARSER_OSH_STUB + [code])
        ast_dict = json.loads(res.decode())
        if ast_dict is None:
            raise self.ParseError("Parser returned None")
        tree = self.load(ast_dict)
        return OshTransformer().visit(tree)

class OshTransformer(NodeTransformer):
    """Does some reshaping on tree. For example, dropping or modifying nodes"""

    def visit_Sentence(self, node):
        return node.child

