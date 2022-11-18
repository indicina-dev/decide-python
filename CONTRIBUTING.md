# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

## Types of Contributions

### Report Bugs

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

You can never have enough documentation! Please feel free to contribute to any
part of the documentation, such as the official docs, docstrings, or even
on the web in blog posts, articles, and such.

### Submit Feedback

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `indicina-decide` for local development.

# Contribution
## Setup Project
The link for this projects's repository can be found [here](decide-python.git)
### Cloning the project

##### For HTTPS
Use this command `git clone https://github.com/indicina-dev/decide-python.git`

##### For SSH
Use this command `git clone git@github.com:indicina-dev/decide-python.git`

#### Running the project
- Create virtual enviroment
- Install the requirements.txt file `pip install -r requirements.txt`
- Run files

## Contribute to Project
Do you find the project interesting and you would like to contribute to our project?
- Fork the repository to your github account
- Clone the repository to your local machine
- Create a new branch for your fix (preferably descriptive to your contribution)
- Make appropriate changes and tests for the changes
- Use `git add insert-paths-of-changed-files-here` to add the file contents of the changed files to the "snapshot" git uses for project management
- Committing: As a means to create a seamless development and contribution flow, we require that commits be standardized, following the conventional [commits guideline](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

We have included the hook script to verify your commits, you will need to install it as follows:
```
pip install pre-commit
pre-commit install --hook-type commit-msg
```

Examples of good commits:
1. adding a new feature: `git commit -m "feat: allow provided config object to extend other configs"`

2. adding a breaking change, take note of the _!_ : `git commit -m "feat!: send an email to the customer when a product is shipped"`
- Push the changes to the remote repository using `git push origin branch-name-here`

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include additional tests if appropriate.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for all currently supported operating systems and versions of Python.
- Submit a pull request to the upstream repository
- Title the pull request with a short description of the changes made and the issue or bug number associated with your change. For example, you can title an issue like so `Added more log outputting to resolve #4352`.
- Wait for our in-house developers to approve the merge requests or update the merge requests if changes were requested,

## Issues
To create an issue, simply click on the issues tab on the menu and create a new issue.

## Code of Conduct

Please note that the `indicina-decide` project is released with a
Code of Conduct. By contributing to this project you agree to abide by its terms.