# Developer Guidelines

Clone this repository locally:
[Instructions](https://github.com/averna-reuse/.github-private/blob/main/profile/getting-started/repo-cloning.md).

It is recommended to create a virtual environment. If you have the project open
in Visual Studio Code, this can be done easily by opening the command palette
(CTRL-SHIFT-P) and searching for _Python: Create Environment..._. This action is
only available if you have installed the python extension in VSCode.

Finally, the required packages need to be installed in the virtual environment.
Open a terminal in Visual Studio Code and execute `pip install -r
requirements.txt` (VSCode activates the virtual environment automatically).

When you change the library, follow
[`docs/developer/change-validation.md`](change-validation.md) to
run the tests, build local packages, and validate them from downstream
projects.
