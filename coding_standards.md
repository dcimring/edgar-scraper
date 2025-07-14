# Python Coding Standards

## 1. Introduction

This document outlines the coding standards and conventions to be followed during the development of the SEC EDGAR Crypto Alert Service. Adhering to these standards ensures code quality, readability, and maintainability.

## 2. Code Formatting

*   **PEP 8:** All Python code must adhere to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).
*   **Automated Formatting:** The `black` code formatter will be used to ensure a consistent style across the entire codebase. A line length of 88 characters will be enforced.
*   **Sorting Imports:** Imports will be automatically sorted using `isort`.

## 3. Naming Conventions

*   **Variables:** `snake_case` (e.g., `filing_text`).
*   **Functions:** `snake_case` (e.g., `get_filing_content`).
*   **Classes:** `PascalCase` (e.g., `SecEdgarClient`).
*   **Modules:** `snake_case` (e.g., `sec_client.py`).
*   **Constants:** `UPPER_SNAKE_CASE` (e.g., `BASE_URL`).

## 4. Type Hinting

*   All function signatures (arguments and return values) must include type hints as specified in [PEP 484](https://www.python.org/dev/peps/pep-0484/).
*   Use the `typing` module for complex types.

Example:
```python
from typing import List, Dict

def process_filings(filings: List[Dict[str, str]]) -> None:
    # function body
    pass
```

## 5. Docstrings

*   All modules, classes, and functions must have docstrings.
*   The [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#3.8-comments-and-docstrings) format for docstrings will be used.

Example:
```python
def example_function(arg1: int, arg2: str) -> bool:
    """This is an example docstring.

    Args:
        arg1: The first argument.
        arg2: The second argument.

    Returns:
        True if successful, False otherwise.
    """
    # function body
    return True
```

## 6. Linting

*   `Ruff` will be used as the primary linter to catch errors and enforce coding standards. It will be configured to be compatible with `black`.

## 7. Testing

*   The `pytest` framework will be used for writing and running tests.
*   All new features and bug fixes must be accompanied by unit tests.
*   Tests should be placed in a `tests/` directory that mirrors the application's package structure.

## 8. Dependency Management

*   Project dependencies will be managed using a `requirements.txt` file. This file will be generated from a `requirements.in` file to pin dependencies.

## 9. Security

*   Sensitive information such as API keys, tokens, and passwords must not be hardcoded in the source code.
*   This information should be loaded from environment variables or a secure configuration management system.

## 10. Version Control

*   All code will be managed in a Git repository.
*   Commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
