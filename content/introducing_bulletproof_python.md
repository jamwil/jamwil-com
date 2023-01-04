+++
title = "Introducing bulletproof-python"
date = "2023-01-02T19:58:00Z"
updated = "2023-01-03T00:13:00Z"
[taxonomies]
tags = ["bulletproof-python", "python", "tooling"]
+++

I owe a debt of gratitude to [Claudio Jolowicz](https://github.com/cjolowicz/)
for introducing me to modern python tooling. His
[Hypermodern Python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)
template and associated blog series are a great resource.

The Hypermodern system is built around [nox](https://nox.thea.codes/en/stable/)
and [poetry](https://python-poetry.org).

- nox is similar in spirit to [tox](https://tox.wiki/en/latest/) but uses python
  scripts instead of configuration files.
- It's very powerful, but since I'm not particularly clever, I find the
  hypermodern stack difficult to understand.

I decided to throw together a simple template that uses tox and pip-tools. The
template uses:

- [pytest](https://docs.pytest.org/en/7.2.x/) and
  [coverage.py](https://coverage.readthedocs.io/en/latest/) for testing,
- [black](https://black.readthedocs.io/en/stable/) for formatting, and
- [ruff](https://github.com/charliermarsh/ruff) for linting.

It strives to be clean, simple and hard to break, albeit incomplete and likely
suitable only for small libraries without broad distribution.

🌱 **The template is available here:
[bulletproof-python](https://github.com/jamwil/bulletproof-python)**.

<!-- more -->

---

Note: The original version of this post incorrectly stated that Poetry does not
play nice with pip-installs from git source. This is not the case; I simply had
my `pyproject.toml` file incorrectly configured to use setuptools instead of
poetry-core as the build backend.
