# Wrap SCT checks -------------------------------------------------------------

from shellwhat.State import State
from shellwhat import checks
import builtins
from protowhat.sct_syntax import create_sct_context

# used in Chain and F, to know what methods are available
sct_dict = {k: v for k,v in vars(checks).items() if k not in builtins.__dict__ if not k.startswith('__')}
SCT_CTX = create_sct_context(State, sct_dict)

# used in test_exercise, so that scts without Ex() don't run immediately
globals().update(SCT_CTX)

# put on module for easy importing
__all__ = list(SCT_CTX.keys())
