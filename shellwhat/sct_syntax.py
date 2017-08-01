from shellwhat.State import State
from shellwhat import checks
import builtins

from protowhat.sct_syntax import create_sct_context

sct_dict = {k: v for k,v in vars(checks).items() if k not in builtins.__dict__ if not k.startswith('__')}
SCT_CTX = create_sct_context(State, sct_dict)

# put on module for easy importing
globals().update(SCT_CTX)
__all__ = list(SCT_CTX.keys())
