# `plox`

Python implementation of the first (java) Interpreter from Robert Nystrom's
[_Crafting Interpreters_](https://craftinginterpreters.com/) book.

# Usage

Install:

```bash
uv venv
source .venv/bin/activate.fish # or whatever for your shell
uv pip install -e .
python plox
```

Or, for testing/dev

```bash
uv venv
source .venv/bin/activate.fish # or whatever for your shell
uv pip install -e .[dev]
pytest
```


