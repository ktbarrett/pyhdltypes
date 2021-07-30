import nox


@nox.session
def tests(session):
    session.install(".")
    session.install("pytest", "pytest-coverage", "coverage")
    session.run("pytest", "--cov=hdltypes", "--cov-branch", "tests/", *session.posargs)
