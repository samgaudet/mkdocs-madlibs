# MkDocs Mad Libs

[![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-madlibs)](https://pypi.org/project/mkdocs-madlibs/)
![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)
[![Documentation Status](https://readthedocs.org/projects/mkdocs-madlibs/badge/?version=latest)](https://mkdocs-madlibs.readthedocs.io/en/latest/?badge=latest)

Code templating with user inputs for PyMdown [_superfences_](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/);
an incarnation of [_Mad Libs_](https://www.madlibs.com/) for your documentation.

## Example

MkDocs Mad Libs is simple to use&mdash;templated inputs are surrounded by triple underscores.

The following markdown code:

````
```madlibs
python
~~~
print("Hello, ___NAME___, welcome to MkDocs Mad Libs!")
```
````

Turns into:

```madlibs
python
~~~
print("Hello, ___NAME___, welcome to MkDocs Mad Libs!")
```

## Installation

`mkdocs-madlibs` is [_distributed through PyPI_](https://pypi.org/project/mkdocs-madlibs/),
and installable via `pip`:

```bash
pip install mkdocs-madlibs
```
