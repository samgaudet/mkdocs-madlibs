import copy
import re

from bs4 import BeautifulSoup
from pymdownx.highlight import Highlight

TRIPLE_UNDERSCORE = "___"
TRIPLE_UNDERSCORE_WORD_PATTERN = re.compile(r'(___.*?___)')
MADLIBS_EDITABLE_CLASS = "madlibs-editable"

def modify_code_block_html(html: str) -> str:
    """Modifies a superfences code block HTML.
    Replaces keywords surrounded by triple-underscores with user inputs.

    Args:
        html (str): The original code block HTML from pymdownx.highlight.

    Returns the modified HTML of the code block as a str.
    """
    soup = BeautifulSoup(html, "html.parser")
    spans = soup.find_all("span")

    for span in spans:
        if span.string and TRIPLE_UNDERSCORE in span.string:
            substrings = TRIPLE_UNDERSCORE_WORD_PATTERN.split(span.string)

            # iterate over the reversed list of substrings
            # so they are added 'in order' when using `insert_after`
            for substring in reversed(substrings):
                duplicated_span = copy.copy(span)

                if substring.startswith(TRIPLE_UNDERSCORE):
                    # add the madlibs custom CSS classes
                    # add list to avoid mutating the underlying list,
                    # which would affect other copies
                    duplicated_span["class"] = (
                        duplicated_span["class"] + [MADLIBS_EDITABLE_CLASS]
                    )
                    # make the text user-editable
                    duplicated_span["contenteditable"] = "true"
                    # select all text on click; stolen from:
                    # https://stackoverflow.com/a/3805897
                    duplicated_span["onClick"] = "document.execCommand('selectAll',false,null)"
                    # disable spellcheck for the contenteditable
                    duplicated_span["spellcheck"] = "false"
                    # add a tooltip for users:
                    duplicated_span["title"] = f"Edit {substring.replace(TRIPLE_UNDERSCORE, '')}"
                    # use the trunder placeholder for the initial span content
                    duplicated_span.string = substring.replace(TRIPLE_UNDERSCORE, "")
                else:
                    duplicated_span.string = substring

                span.insert_after(duplicated_span)

            # remove the original span that has been split
            span.extract()

    modified_html = str(soup.prettify())
    return modified_html

def fence(
    source: str,
    language,
    css_class,
    options,
    md,
    classes=None,
    id_value="",
    attrs=None,
    **kwargs,
) -> str:
    """Custom fencer for madlibs-style code blocks.
    These code blocks include user inputs for specified keywords.

    Args:
        source (str): The markdown source of the code block.

    Returns:
        The code block source as an HTML str.
    """
    parsed_source = source.split("~~~")

    _language = parsed_source[0].strip()
    _source = parsed_source[1].strip()

    highlighter = Highlight()
    code_block = highlighter.highlight(
        src=_source,
        language=_language,
        classes=[f"language-{_language}.highlight"],
    )

    modified_html = modify_code_block_html(code_block)

    return modified_html
