from protowhat.selectors import Dispatcher
from protowhat.State import State as BaseState
from shellwhat.parsers import DEFAULT_PARSER


class State(BaseState):
    def get_dispatcher(self):
        return Dispatcher.from_module(DEFAULT_PARSER)
