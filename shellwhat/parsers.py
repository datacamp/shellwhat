from protowhat.utils_ast import AstNode, AstModule
from ast import NodeTransformer
from subprocess import check_output
import json
import os


class OshNode(AstNode):
    def get_text(self, full_text=None):
        if self.text:
            return self.text
        else:
            raise RuntimeError("The parser wasn't able to match text to this node")

    def get_position(self):
        return self.position


class OshParser(AstModule):
    AstNode = OshNode

    @classmethod
    def parse(cls, code, strict=True):
        try:
            res = check_output(
                PARSER_OSH_STUB + [code],
                env=dict(os.environ, PYENV_VERSION="2.7.10", PYTHONPATH=PYTHONPATH),
            )
            ast_dict = json.loads(res.decode())
            if ast_dict is None:
                raise cls.ParseError("Parser returned None")
        except:
            raise cls.ParseError("Parser failed")
        tree = cls.load(ast_dict)
        return OshTransformer().visit(tree)

    @classmethod
    def dump(cls, tree):
        node = super().dump(tree)
        if isinstance(node, dict):
            node["text"] = tree.text
            node["position"] = tree.position
        return node

    @classmethod
    def load(cls, node):
        obj = super().load(node)
        if isinstance(obj, cls.AstNode):
            obj.text = node.get("text")
            obj.position = node.get("position")
        return obj


class OshTransformer(NodeTransformer):
    """Reshaping on tree, for example, dropping or modifying nodes"""

    pass


class DummyParser(AstModule):
    @classmethod
    def parse(cls, *args, **kwargs):
        raise cls.ParseError


# Determine which parser to use and how it is called.
# By default, the DummyParser is used.
parse_opt = os.environ.get("SHELLWHAT_PARSER", "osh")
PYTHONPATH = "/var/lib/python/site-packages/python2"
if parse_opt == "osh":
    DEFAULT_PARSER = OshParser
    PARSER_OSH_STUB = ["python2", "-m", "osh"]
elif parse_opt == "docker":
    DEFAULT_PARSER = OshParser
    PARSER_OSH_STUB = ["docker", "exec", "oilc", "python2", "-m", "osh"]
else:
    DEFAULT_PARSER = DummyParser
