# Contributing

We welcome contributions for new features, bug fixes, additional examples, tutorials and documentation.

All contributions should be provided via a pull request with a short description of what they provide.

## Reporting Bugs

Please report all bugs via the GitHub repository issue tracker. Please include a reproducible code snippet and a description of the cause and impact of the bug.

## Coding Standards

### Overview

This section specifies the minimum standards we expect for code contributions.

In short, a set of tasks is described for a nox pipeline. These are described in `noxfile.py` and consist of testing, linting and documenting. Code submissions should be accompanied by appropriate unit tests, should not have failing tests, should conform to PEP8 standards and should not fail linting. Methods and classes should have docstrings formatted according to the NumPy docstring format.

### Documentation

* All classes and methods must be documented. Docstrings should be provided. PanaXea adopts the [NumPy Docstring Format](https://numpydoc.readthedocs.io/en/latest/format.html);
* Comments should be appropriately formatted such that sphinx may be able to generate HTML documentaiton by calling `make html` in the docs directory;

### Testing

* No tests should be failing;
* New tests should be added for new functionalities, where appropriate old ones should be updated;
* Tests should be runnable by calling `pytest` from the root directory;

### Code Formatting

* PEP8 guidelines should be adhered to. No lint warnings/errors should be displayed when calling `flake8` on any module/test directory.

## Acknowledgements

All contributors will be acknowledged in the [Authors](authors.md) file.
