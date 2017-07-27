from sqlwhat.State import State as BaseState

class State(BaseState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # just in case the code is valid postgresql, set as if couldn't parse.
        self.solution_ast = self.student_ast = self.ast_dispatcher.ast.AntlrException('', '')

    def get_dialect(self):
        return 'postgresql'
