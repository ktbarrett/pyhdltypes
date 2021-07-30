import nox


@nox.session
def tests(session):
    session.install(".")
    session.install("pytest", "pytest-coverage", "coverage", "pytest-mypy-plugins")
    session.run("pytest", "--cov=hdltypes", "--cov-branch", *session.posargs)
