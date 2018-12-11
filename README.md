shellwhat
=========

[![Build Status](https://travis-ci.org/datacamp/shellwhat.svg?branch=master)](https://travis-ci.org/datacamp/shellwhat)
[![codecov](https://codecov.io/gh/datacamp/shellwhat/branch/master/graph/badge.svg)](https://codecov.io/gh/datacamp/shellwhat)
[![PyPI version](https://badge.fury.io/py/shellwhat.svg)](https://badge.fury.io/py/shellwhat)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdatacamp%2Fshellwhat.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdatacamp%2Fshellwhat?ref=badge_shield)

`shellwhat` enables you to write Submission Correctness Tests (SCTs) for interactive Shell exercises on DataCamp.

- If you are new to teaching on DataCamp, check out https://instructor-support.datacamp.com.
- If you want to learn what SCTs are and how they work, visit [this article](https://instructor-support.datacamp.com/courses/course-development/submission-correctness-tests) specifically.
- For a complete overview of all functionality inside `shellwhat` and articles about what to use when, consult https://shellwhat.readthedocs.io.

Installing
----------

```
pip install shellwhat
```

Development
-----------

By default, the `DummyParser` is used, that does not parse the shell code.
Hence, you can not run tests that need this parser:

```
pytest -m "not osh"
```

If you also want to run these 'parser tests',
there is Dockerfile to parse shell commands with
the [Oil parser](https://github.com/oilshell/oil):

```
# Look in Makefile for details
export SHELLWHAT_PARSER='docker'
make test
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdatacamp%2Fshellwhat.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdatacamp%2Fshellwhat?ref=badge_large)