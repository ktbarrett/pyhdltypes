import nox


@nox.session
def tests(session: nox.Session) -> None:
    session.install("-r", ".test-reqs.txt")
    session.install(".")
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


@nox.session(reuse_venv=True)
def dev(session: nox.Session) -> None:
    session.install("-r", ".check-reqs.txt")
    session.install("-r", ".test-reqs.txt")
    session.install("-e", ".")
    session.run("bash", external=True)
