from protowhat.selectors import Dispatcher
from protowhat.State import State as BaseState

from protowhat.utils_ast import AstModule


from subprocess import check_output
import shlex
import json

PARSER_OSH_STUB = ["python2", "-m", "osh"]
#PARSER_OSH_STUB = ["docker", "exec", "oilc", "python2", "-m", "osh"]

def parse_osh(cmd, strict = False):
    res = check_output(PARSER_OSH_STUB + [cmd])
    return json.loads(res.decode())

class State(BaseState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_dispatcher(self):
        ast_mod = AstModule.from_parse_dict(parse_osh)
        return Dispatcher(ast_mod.classes, ast_mod)
        
