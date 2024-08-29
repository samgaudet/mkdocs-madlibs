import copy
import re

from bs4 import BeautifulSoup, PageElement, NavigableString
from pymdownx.highlight import Highlight

TRIPLE_UNDERSCORE = "___"
TRIPLE_UNDERSCORE_WORD_PATTERN = re.compile(r"(___.*?___)")
MADLIBS_EDITABLE_CLASS = "madlibs-editable"


def prepare_madlibs_element(
    element: PageElement,
    substring: str,
) -> PageElement:
    """Prepare the MkDocs Madlibs element, including
    - Strip the element's content of triple underscores.
    - Set the `title` to the Tag as a tooltip for users.
    - Add the `madlibs-editable` CSS class to the Tag.
    - Set the `contenteditable` attribute to `true` to allow user editing.
    - Set the `onClick` behavior to select all text when clicked.
    - Set `spellcheck` to `false` to avoid visual bugs with spelling errors.

    Args:
        element (PageElement): The Tag element that contains the content that
            should be editable.
        substring (str): The substring of text that should be the content.

    Returns:
        The updated PageElement to be added to a Soup.
    """
    element.string = substring.replace(TRIPLE_UNDERSCORE, "")
    element["title"] = f"Edit {substring.replace(TRIPLE_UNDERSCORE, '')}"
    if getattr(element, "class"):
        # if there are already CSS classes present:
        # add list to avoid mutating the underlying list,
        # which would affect other copies
        element["class"] = element["class"] + [MADLIBS_EDITABLE_CLASS]
    else:
        element["class"] = [MADLIBS_EDITABLE_CLASS]
    element["contenteditable"] = "true"
    # select all text on click; stolen from:
    # https://stackoverflow.com/a/3805897
    element["onClick"] = "document.execCommand('selectAll',false,null)"
    element["spellcheck"] = "false"

    return element


def modify_code_block_html(html: str) -> str:
    """Modifies a superfences code block HTML.
    Replaces keywords surrounded by triple-underscores with user inputs.

    Args:
        html (str): The original code block HTML from pymdownx.highlight.

    Returns the modified HTML of the code block as a str.
    """
    soup = BeautifulSoup(html, "html.parser")
    code = soup.find("code")

    for element in code.contents:
        if isinstance(
            element, NavigableString
        ) and TRIPLE_UNDERSCORE_WORD_PATTERN.search(element):
            substrings = TRIPLE_UNDERSCORE_WORD_PATTERN.split(element)

            # iterate over the reversed list of substrings
            # so they are added 'in order' when using `insert_after`
            for substring in reversed(substrings):
                # annoyingly, we have to check for empty substrings
                if substring and substring.startswith(TRIPLE_UNDERSCORE):
                    new_span = soup.new_tag("span")
                    new_span = prepare_madlibs_element(new_span, substring)
                    element.insert_after(new_span)
                elif substring:
                    new_element = NavigableString(substring)
                    element.insert_after(new_element)
                else:
                    pass

            # remove the original span that has been split
            element.extract()

        elif (
            element.name == "span"
            and element.string
            and TRIPLE_UNDERSCORE_WORD_PATTERN.search(element.string)
        ):
            substrings = TRIPLE_UNDERSCORE_WORD_PATTERN.split(element.string)

            # iterate over the reversed list of substrings
            # so they are added 'in order' when using `insert_after`
            for substring in reversed(substrings):
                duplicated_span = copy.copy(element)

                if substring.startswith(TRIPLE_UNDERSCORE):
                    duplicated_span = prepare_madlibs_element(
                        duplicated_span, substring
                    )
                else:
                    duplicated_span.string = substring

                element.insert_after(duplicated_span)

            # remove the original span that has been split
            element.extract()
        else:
            pass

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
