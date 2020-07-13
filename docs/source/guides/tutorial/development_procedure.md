# Development Procedure

### Installation

Please follow [Lego 3 - installation guide](./installation_guide.md).

### Source and Tasks Control

Each Lego issue should be well documented on [Lego](https://trello.com/b/N1MDT9Lr/lego) Trello page.

How to contribute to Lego?

1. Select an issue to work on from the `to do` column.
2. Join your account to this issue.
3. Create a new branch in GitHub with the same name as the issue.
4. Join the branch to the issue using the GitHub extension.
5. Move the issue to the `WIP` column.
6. Develop a new feature (following the below instructions).
7. Open a PR in GitHub, and move the issue to `Review` column.
8. Repeat 7-8 phases until the PR approved.
9. Merge your branch and delete it.
10. Move the issue to the `Done` column.

> **Note:** Any contribution of new code to `master` branch should pass the process of PR -> CR.
> this is in purpose to keep the repository clean and order, and make sure the contributed code doesn't harm any other code first, and second - do what it suppose to do.
> Up to now, the permission to merge to `master` can give by one of us: [Ariel Chinn](https://github.com/yelly), [Steven Dashevsky](https://github.com/Steven17D) and [Elyashiv Shayovitz](https://github.com/Elyash).

### Development

#### Pylint and MyPy

Please follow [Lego 3 - configurations guide](../configurations/conventions_linters.md).

#### Conventions

Please follow our [Lego 3 - conventions guide](./conventions_guide.md).

### IDEs

Please follow the [Lego 3 - development helpers](../development_helpers/developer_helpers.md)
and read the *extensions_guide* of your favorite IDE.
