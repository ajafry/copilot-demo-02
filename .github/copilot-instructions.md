# Project Guidelines

## Code Style

- **Python 3.13+** — use modern Python idioms and syntax.
- Follow **PEP 8** for formatting, naming, and layout.
- Use **type hints** on all function signatures and return types.
- Prefer **f-strings** over `str.format()` or `%` formatting.

## Constants & Magic Numbers

- **Never use magic numbers or magic strings** inline in code. Define them as named constants at the module level (e.g., `MAX_RETRIES = 3`).
- Group related constants together near the top of the module or in a dedicated `constants.py` file.
- Use `enum.Enum` or `enum.IntEnum` for finite sets of related values.

## Naming Conventions

- **Variables & functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private/internal**: prefix with a single underscore `_`

## Best Practices

- Keep functions small and focused — each function should do one thing.
- Prefer **early returns** over deeply nested `if/else` blocks.
- Use **list/dict/set comprehensions** where they improve readability; avoid overly complex one-liners.
- Handle exceptions specifically — never use bare `except:`.
- Use `pathlib.Path` instead of `os.path` for file system operations.
- Use **context managers** (`with` statements) for resource management.
- Avoid mutable default arguments in function signatures.

## Imports

- Group imports in order: **stdlib → third-party → local** (separated by blank lines).
- Use absolute imports; avoid wildcard imports (`from module import *`).

## Testing

- Write tests using **pytest**.
- Name test files `test_<module>.py` and test functions `test_<behavior>`.
- Each test should be independent and test a single behavior.

## Documentation

- Add docstrings to public modules, classes, and functions.
- Use concise, imperative-mood descriptions (e.g., "Return the factorial of n.").
