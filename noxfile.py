import nox

@nox.session(python=["3"])
def test(session):
    session.install("pytest")
    session.run("pytest")

@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "./panaxea")
    session.run("flake8", "./tests")
    session.run("flake8", "./examples")

@nox.session
def document(session):
    session.install("sphinx")
    session.install("sphinx_rtd_theme")
    session.run("python", "-c", "\"import sys\"")
    session.run("python", "-c", "\"import os\"")
    session.run("python", "-c", "\"sys.path.insert(0, os.path.abspath("
                                "'../../core'))\"")
    session.run("python", "-c", "\"sys.path.insert(1, os.path.abspath("
                                "'../../toolkit'))\"")
    session.run("python", "-c", "\"sys.path.insert(2, os.path.abspath("
                                "'../..'))\"")
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/build")
