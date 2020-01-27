from protowhat.Feedback import Feedback as ProtoFeedback


class Feedback(ProtoFeedback):
    ast_highlight_offset = {
        "line_start": 1,
        "column_start": 1,
        "line_end": 1,
        "column_end": 0,
    }
