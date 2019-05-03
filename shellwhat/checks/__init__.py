from shellwhat.checks.has_funcs import (
    has_code,
    has_output,
    has_cwd,
    has_expr_output,
    has_expr_exit_code,
)

from protowhat.checks.check_logic import fail, multi, check_not, check_or, check_correct
from protowhat.checks.check_simple import has_chosen, success_msg
from protowhat.checks.check_files import check_file, has_dir

# be cautious using protowhat checks
# has_code has its own implementation in shellwhat
from protowhat.checks.check_funcs import (
    check_node,
    check_edge,
    has_equal_ast,
    has_parsed_ast,
)
from protowhat.utils import _debug
