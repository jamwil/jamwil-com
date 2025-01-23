+++
title = "How to convert a subdirectory to its own git repository/submodule"
date = "2023-01-12T15:53:00Z"
[taxonomies]
tags = ["development", "git", "submodules", "version-control", "workflow"]
categories = ["Technology"]
+++

```bash
# Make a clone of the repository
git clone <your_project> <new_submodule>

# CD into the new repository
cd <new_submodule>

# Use filter-branch to isolate the subdirectory
git filter-branch --subdirectory-filter 'path/to/subdirectory' --prune-empty -- --all

# Remove the old remote
git remote rm <remote_name>
```

`git filter-branch` lets you rewrite Git revision history and apply custom
filters on each revision. **It should be used with caution!** From the Git
Manual (emphasis mine):

> git filter-branch has a plethora of pitfalls that can produce non-obvious
> manglings of the intended history rewrite (and can leave you with little time
> to investigate such problems since it has such abysmal performance). These
> safety and performance issues cannot be backward compatibly fixed and as such,
> **its use is not recommended**.

Nevertheless, since we live dangerously around these parts, here's what's
happening with the filter-branch command should you choose to use it:

- `--subdirectory-filter` is the main command. It takes a path to a subdirectory
  and filters the repository to only include that subdirectory.
- `--prune-empty` removes commits that don't change anything.
- `-- --all` is a way to pass arguments to the internal `git rev-list` command.
  In this case, it's telling git to run the command on all branches.

Once the operation is done, you'll have a new repository with only the
subdirectory you specified. You can then push it to a new remote and add it as a
submodule to your original repository.

`git filter-branch` is a destructive operation. While I've used the above
command with success on my own repositories, your mileage may vary and I
probably can't help you if something goes wrong.

<!-- more -->
