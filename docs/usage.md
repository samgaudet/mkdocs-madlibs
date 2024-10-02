# Usage

## Configuration

### Install `mkdocs-madlibs` as a dependency

`mkdocs-madlibs` must be installed as a Python dependency in the environment used to build or run your MkDocs site.
`mkdocs-madlibs` is distributed via PyPI and is installable via `pip`:

```bash
pip install mkdocs-madlibs
```

### Add custom fence definition

`mkdocs-madlibs` implements a [_custom fence_](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/#custom-fences).
The custom fence is defined in your `mkdocs.yml` file:

```yaml title="mkdocs.yml"
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: madlibs
          class: madlibs
          format: !!python/name:mkdocs_madlibs.fence
```

### Add custom CSS dependency

`mkdocs-madlibs` uses custom CSS to style the user inputs of a "Mad Libs" code block.
The custom CSS dependencies must be added to your documentation directory, and referenced in your `mkdocs.yml` file:

```yaml title="mkdocs.yml"
extra_css:
  - stylesheets/extra.css
```

Copy or download the content of the CSS file here:
[**extra.css**](https://raw.githubusercontent.com/samgaudet/mkdocs-madlibs/main/docs/stylesheets/extra.css).

## Utilization

Once configured, `mkdocs-madlibs` custom fences are a breeze to use.
Fenced code is defined using three backticks (\`\`\`) as normal.
Within the fenced code, the language to use for highlighting is defined first, followed by three tildes (~~~).
Following the language and three tildes (~~~), the code content to display is included.
`mkdocs-madlibs` uses triple-underscores (affectionately known as '_trunder_ syntax') to denote items that should be a user input.

The following fenced code:

````
```madlibs
python
~~~
print("Hello, ___NAME___.")
```
````

Renders this interactive code block when using `mkdocs-madlibs`:

```madlibs
python
~~~
print("Hello, ___NAME___.")
```

### Underscore alternative

Occasionally, escaping a Mad Libs word with underscores is not possible if the word is surrounded by one or more underscores.
In these instances, surround the word to replace with three carets (^^^) instead.

The following fenced code:

````
```madlibs
text
~~~
hello_my_name_is_^^^NAME^^^
```
````

Renders this interactive code block when using `mkdocs-madlibs`:

```madlibs
text
~~~
hello_my_name_is_^^^NAME^^^
```

### Adding a title

MkDocs Mad Libs supports [adding titles](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-a-title).
However, attributes are only passed to the MkDocs Mad Libs formatter if an attribute style header is used.
In order to use an attribute style header, you must first enable the
[_Attribute Lists_ extension](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/#attribute-lists).

The following fenced code:

````md
```{.madlibs title="Hello world example"}
python
~~~
print("Hello, ___NAME___.")
```
````

Renders this interactive code block when using `mkdocs-madlibs`:

```{.madlibs title="Hello world example"}
python
~~~
print("Hello, ___NAME___.")
```

### Highlighting specific lines

MkDocs Mad Libs supports [highlighting specific lines](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#highlighting-specific-lines).
However, attributes are only passed to the MkDocs Mad Libs formatter if an attribute style header is used.
In order to use an attribute style header, you must first enable the
[_Attribute Lists_ extension](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/#attribute-lists).

The following fenced code:

````md
```{.madlibs hl_lines="1-2 5"}
python
~~~
def greet(name: str) -> None:
    print(f"Hello, {name}.")

if __name__ == "__main__":
    greet("___NAME___")
```
````

Renders this interactive code block when using `mkdocs-madlibs`:

```{.madlibs hl_lines="1-2 5"}
python
~~~
def greet(name: str) -> None:
    print(f"Hello, {name}.")

if __name__ == "__main__":
    greet("___NAME___")
```
