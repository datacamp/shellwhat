from protowhat.utils_ast import AstModule
from ast import NodeTransformer
from subprocess import check_output
import json
import os

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

# Determine which parser to use and how it is called.
# By default, the DummyParser is used.
parse_opt = os.environ.get('SHELLWHAT_PARSER')
if parse_opt == 'osh':
    DEFAULT_PARSER = OshParser
    PARSER_OSH_STUB = ["python2", "-m", "osh"]
elif parse_opt == 'docker':
    DEFAULT_PARSER = OshParser
    PARSER_OSH_STUB = ["docker", "exec", "oilc", "python2", "-m", "osh"]
else:
    DEFAULT_PARSER = DummyParser
