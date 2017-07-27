from sqlwhat.sct_syntax import SCT_CTX, ATTR_SCTS, state_dec
import sqlwhat

from shellwhat.State import State

# Since the sct_syntax module imports sqlwhat's State, and uses it in functions
# like state_dec, we need to replace that reference to State w/ shellwhat's version
# this means that we can use all the SCTs in sqlwhat, with the state from shellwhat
# TODO: generalize sqlwhat.sct_syntax for protowhat
sqlwhat.sct_syntax.State = State

from shellwhat.checks import test_output_contains
ATTR_SCTS['test_output_contains'] = test_output_contains
SCT_CTX['test_output_contains'] = state_dec(test_output_contains)
