shellwhat
=========

[![Build Status](https://travis-ci.org/datacamp/shellwhat.svg?branch=master)](https://travis-ci.org/datacamp/shellwhat)
[![codecov](https://codecov.io/gh/datacamp/shellwhat/branch/master/graph/badge.svg)](https://codecov.io/gh/datacamp/shellwhat)
[![PyPI version](https://badge.fury.io/py/shellwhat.svg)](https://badge.fury.io/py/shellwhat)

`shellwhat` enables you to write Submission Correctness Tests (SCTs) for interactive Shell exercises on DataCamp.

- If you are new to teaching on DataCamp, check out https://authoring.datacamp.com.
- If you want to learn what SCTs are and how they work, visit [this article](https://authoring.datacamp.com/courses/exercises/technical-details/sct.html) specifically.
- For a complete overview of all functionality inside `shellwhat` and articles about what to use when, consult https://shellwhat.readthedocs.io.

Installing
----------

```
pip install shellwhat
```

Development
-----------

Without the Osh parser ...

```
export SHELLWHAT_PARSER='0'
pytest -m "not osh"
```

With the Osh parser using docker ...

```
# install osh parser docker image
make dev
export SHELLWHAT_PARSER='docker'

# run tests
pytest
```
