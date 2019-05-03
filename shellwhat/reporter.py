from protowhat.Reporter import Reporter as BaseReporter


class Reporter(BaseReporter):
    ast_highlight_offset = {
        "line_start": 1,
        "column_start": 1,
        "line_end": 1,
        "column_end": 0,
    }
