import nox


@nox.session
def tests(session):
    session.install(".")
    session.install("pytest", "pytest-coverage", "coverage", "pytest-mypy-plugins")
    session.run("pytest", "--cov=hdltypes", "--cov-branch", *session.posargs)
    session.run("coverage", "xml")


@nox.session
def docs(session):
    session.install(".")
    session.install("-r", "docs/requirements.txt")
    session.run("sphinx-build", "docs/", "docs_out/", *session.posargs)
