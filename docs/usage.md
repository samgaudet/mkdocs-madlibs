# Usage

## Configuration

### Install `mkdocs-madlibs` as a dependency

`mkdocs-madlibs` must be installed as a Python dependency in the environment used to build or run your MkDocs site.
`mkdocs-madlibs` is distributed via PyPI and installable via `pip`:

```bash
pip install mkdocs-madlibs
```

### Add custom fence definition

`mkdocs-madlibs` implements a [_custom fence_](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/#custom-fences).
The custom fence is defined in your `mkdocs.yml` file:

```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: madlibs
          class: madlibs
          format: !!python/name:mkdocs_madlibs.fence
```

### Add custom JavaScript and CSS dependencies

`mkdocs-madlibs` uses custom JavaScript and CSS to style the user inputs of a "Mad Libs" code block.
These custom JavaScript and CSS dependencies must be defined in your `mkdocs.yml` file:

```yaml
extra_javascript:
  - javascripts/extra.js
extra_css:
  - stylesheets/extra.css
```

## Utilization

Once configured, `mkdocs-madlibs` custom fences are a breeze to use.
Fenced code is defined using three backticks (```) as normal.
Within the fenced code, the language to use for highlighting is defined first, followed by three tildes (~~~).
Following the language and three tildes (~~~), the code content to display is included.
`mkdocs-madlibs` uses triple-underscores (affectionately known as '_trunder_ syntax') to denote items that should be a user input.

````
```madlibs
python
~~~
print("Hello, ___NAME___.")
```
````
