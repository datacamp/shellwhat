# Changelog

All notable changes to the shellwhat project will be documented in this file.

## 1.0.0

- All functions that start with `test_` have been deprecated.
- A lot of functions have been renamed. There is now:
    - `has_code()`
    - `has_output()`
    - `has_expr_output()`
    - `has_expr_error()`
- Pull in a lot of utility functions from `protowhat`:
    - `Ex()`
    - `check_or()`, `check_correct()`, `check_not()` and `multi()`
    - `has_chosen()` and `success_msg()`
    - `check_file()` and `has_dir()`
- `has_cwd()` has been added to test the current directory.
- Documentation:
    - Improve reference documentation with examples and caveats.
    - Include functions from `protowhat`.
    - Glossary article with examples for shell and git.
- Improve package structure, test structure and test coverage.
