# name_matching

A tiny example package demonstrating the `src` layout.

## Development

Create a virtual environment and install the project with its dependencies:

```bash
uv venv
source .venv/bin/activate
uv sync
```

### Linting and tests

Use [`nox`](https://nox.thea.codes/) to run lint and test sessions:

```bash
nox -s lint
nox -s tests
```

## Usage

Run the program using the installed command or module:

```bash
name-matching
# or
python -m name_matching
```

Both print `Hello from name-matching!`.

