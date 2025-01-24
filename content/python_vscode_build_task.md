+++
title = "How to configure a python script as the default build task in VS Code"
date = "2023-01-03T22:42:00Z"
[taxonomies]
tags = ["black", "development", "python", "ruff", "testing", "tooling", "vscode"]
categories = ["Technology"]
+++

This snippet goes in your `.vscode/tasks.json` file. It will run the current
python file as the default build task.

- `command` will invoke the python interpreter that is configured in your
  workspace settings.
- `group` will make this task the default build task.
- `presentation:focus` will focus the terminal window when the task is run.
- `presentation:reveal` will reveal the terminal window when the task is run.

Change `args` to any python file if you'd like to run the same file each time.

```json
{
  // See https://go.microsoft.com/fwlink/?LinkId=733558
  // for the documentation about the tasks.json format
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Python: current file",
      "type": "shell",
      "command": "${command:python.interpreterPath}",
      "args": ["${file}"],
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "focus": true,
        "reveal": "always"
      },
      "options": {
        "cwd": "${workspaceFolder}"
      }
    }
  ]
}
```

<!-- more -->
