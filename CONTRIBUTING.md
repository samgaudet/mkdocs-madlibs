# Contributing

Community contributions are welcome and appreciated!
Use this guide for help getting started making a contribution to `mkdocs-madlibs`.

## Understand how custom fencers work

Start by checking out `superfence`'s documentation on
[custom fences here](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/#custom-fences)
for a background on the core functionality provided by `mkdocs-madlibs`.

## Setting up your local environment

You can run the MkDocs content included in this repo locally as a test of your changes.
To do this, it may be easiest to make the local repository importable as a module in Python.
There are several ways to accomplish this, one of which is to create a virtual environment,
and add the path to your local repository (e.g. `C:\Users\sgaud\git\mkdocs-madlibs`) to a `.pth` file in your virtual environment's `site-packages` directory.

## Run the package documentation locally

If you are working in a virtual environment (or similar) and you have
[set up your local environment to import from the local repository](#setting-up-your-local-environment),
you should be able to run the documentation locally,
importing `mkdocs-madlibs` functionality from the local repository itself.
This makes testing changes to the custom fence very simple.

Once you have made changes, start up the documentation locally to test changes:

```bash
python -m mkdocs serve
```

## Ensure your changes meet the repository's quality requirements

Pull requests must pass the test steps defined in the
[`test.yml` GitHub Action](https://github.com/samgaudet/mkdocs-madlibs/blob/main/.github/workflows/test.yml).
To make your development easier, install the requirements in
[`requirements-test.txt`](https://github.com/samgaudet/mkdocs-madlibs/blob/main/requirements-test.txt)
that are used by the GitHub Action,
and run the linting, formatting, and testing steps locally before creating a pull request.
