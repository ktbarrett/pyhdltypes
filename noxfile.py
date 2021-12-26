import nox


@nox.session
def tests(session: nox.Session) -> None:
    session.install(".")
    session.install("pytest", "pytest-coverage", "coverage", "pytest-mypy-plugins")
    session.run(
        "pytest",
        "--cov=hdltypes",
        "--cov-branch",
        "--doctest-modules",
        "src/",  # src/ **MUST** come before test due to issue with doctest-modules
        "tests/",
        *session.posargs
    )
    session.run("coverage", "xml")


@nox.session
def docs(session: nox.Session) -> None:
    session.install(".")
    session.install("-r", "docs/requirements.txt")
    session.run("sphinx-build", "docs/", "docs_out/", *session.posargs)


@nox.session
def dev(session: nox.Session) -> None:
    session.install("isort", "black", "mypy", "flake8", "nox")
    session.install("-e", ".")
    session.run("bash", external=True)


@nox.session(reuse_venv=True)
def fix(session: nox.Session) -> None:
    session.install("isort", "black")
    session.run("isort", "--profile=black", ".")
    session.run("black", ".")
