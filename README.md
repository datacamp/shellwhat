shellwhat
=========

Development
-----------

Without the Osh parser ...

```
export SHELLWHAT_PARSER='0'
py.test -m "not osh"
```

With the Osh parser using docker ...

```
# install osh parser docker image
make dev
export SHELLWHAT_PARSER='docker'

# run tests
py.test
```

