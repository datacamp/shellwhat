from protowhat.utils_ast import AstModule
from ast import NodeTransformer
from subprocess import check_output
import json

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

class DummyParser(AstModule):
    def parse(self, *args, **kwargs):
        return None

# Set defaults for customizing how which parser is used,
# and how OSH is called
import os
parse_opt = os.environ.get('SHELLWHAT_PARSER')

DEFAULT_PARSER = DummyParser if parse_opt == '0' else OshParser
print(DEFAULT_PARSER)
PARSER_OSH_STUB = ["python2", "-m", "osh"]

if parse_opt == 'docker':
    PARSER_OSH_STUB = ["docker", "exec", "oilc"] + PARSER_OSH_STUB

