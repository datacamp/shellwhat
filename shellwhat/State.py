from protowhat.State import State as BaseState

class State(BaseState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_dispatcher(self):
        return None
