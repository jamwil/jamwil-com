+++
title = "How to checkout and edit a pull request locally"
date = "2023-07-16T16:18:00Z"
[taxonomies]
tags = ["git"]
categories = ["Technology"]
+++

Let's say you have a dependabot pull request and Charlie Marsh has added a new
check to [Ruff](https://github.com/astral-sh/ruff) that causes your lint check
to fail. You can fix the lint error and push the changes back to the pull
request branch!

First, checkout the pull request locally:

```bash
# In this case, I'm updating ruff to v0.0.278
git fetch origin dependabot/pip/ruff-0.0.278
git switch --track origin/dependabot/pip/ruff-0.0.278
```

We've now checked out the PR branch and set it to track the remote. We can use
this pattern to keep tabs on long-running PRs, or as in this case, simply push
an additional patch before merging. If you'd like a more friendly local branch
name, you can append the `:my-branch-name` to the end of the git fetch call, and
then call `git switch my-branch-name` to check it out; just keep in mind that
this won't set the local branch to track the remote.

In my case, this ruff release does not provide any new rule categories and my
lints still pass, however I'd like to update the ruff version in my
`.pre-commit-config.yaml` file so that it's consistent with my
`requirements.txt`. I'll make that change, commit and push back to the remote.

```bash
git add .pre-commit-config.yaml
git commit -m "Update pre-commit config."
git push
```

At this point, your checks should fire again and you can merge using your
preferred merge method into your trunk. Check out
[real pull request](https://github.com/jamwil/bulletproof-python/pull/129) to
see how this looks server side.

<!-- more -->
