#!/usr/bin/env python

import sys
import os
from git import Repo
from git.exc import InvalidGitRepositoryError

def fail(msg, exc=None):
    exc = ': {}'.format(exc) if exc else ''
    sys.stderr.write(msg + exc + '\n')
    sys.exit(1)

def print_log(branch):
    print('branch {}'.format(branch))
    actions = [entry[-1].split(': ', 2) for entry in reversed(branch.log())]
    for act in actions:
        print(act)

path = sys.argv[1] if len(sys.argv) > 1 else os.curdir
try:
    repo = Repo(path)
except InvalidGitRepositoryError as e:
    fail('bad repository path', e)

print('repo.bare {}'.format(repo.bare))
print('repo.is_dirty() {}'.format(repo.is_dirty()))
print('repo.untracked_files {}'.format(', '.join(repo.untracked_files)))
print('repo.branches {}'.format(', '.join([str(x) for x in repo.branches])))

print_log(repo.active_branch)
if repo.active_branch.name != 'master':
    print_log(repo.branches['master'])

hc = repo.head.commit
print('head commit {0}'.format(hc))
print('...head commit message {0}'.format(repr(hc.message)))
print('...head commit blobs {0}'.format([b.path for b in hc.tree.blobs]))
content = str(hc.tree.blobs[0].data_stream.read(), 'utf-8')
print('...head commit blobs[0] content\n---\n{0}\n---'.format(content))
