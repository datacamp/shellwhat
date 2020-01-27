# Changelog

All notable changes to the shellwhat project will be documented in this file.

## 1.4.0

- Use protowhat v2
- Expose `has_command` function
- Fix `run()` function

## 1.3.0

- Add `run()` sct function

## 1.2.0

- Update parsing functionality
- Expose `_debug` function
- Update protowhat

## 1.1.1

- Include student code in result payload.

## 1.1.0

- Add optional `force_diagnose` parameter to `test_exercise` to force passing the `diagnose` tests in `check_correct`.

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

