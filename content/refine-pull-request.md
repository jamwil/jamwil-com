+++
title = "How to checkout and refine a pull request locally"
date = "2023-06-22T15:15:23Z"
draft = true
[taxonomies]
tags = ["git", "howto"]
+++

Let's say you have a dependabot pull request and Charlie Marsh has added a new
check to [Ruff](https://github.com/astral-sh/ruff) that causes your lint check
to fail. You can fix the lint error and push the changes back to the pull
request branch!

First, checkout the pull request locally:

```bash
# In this case, I'm updating ruff to v0.0.274
git fetch origin dependabot/pip/ruff-0.0.274:ruff-0.0.274
git switch ruff-0.0.274
```

...TK need to see how to push back to dependabot branch
