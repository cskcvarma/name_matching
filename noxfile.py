import nox

@nox.session
def lint(session) -> None:
    session.install("ruff")
    # Check code style and lint errors
    session.run("ruff", "check", "src", "tests")
    # Verify code is formatted with ruff
    session.run("ruff", "format", "--check", "src", "tests")

@nox.session
def tests(session) -> None:
    session.install("pytest", "pytest-cov")
    session.install("-e", ".")
    session.run("pytest")
