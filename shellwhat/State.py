from protowhat.selectors import Dispatcher
from protowhat.State import State as BaseState
from shellwhat.parsers import OshParser

class State(BaseState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_dispatcher():
        ast_mod = OshParser()
        return Dispatcher(ast_mod.classes, ast_mod)
        
