import copy
import re

from bs4 import BeautifulSoup, PageElement, NavigableString
from pymdownx.highlight import Highlight

TRIPLE_UNDERSCORE = "___"
TRIPLE_UNDERSCORE_WORD_PATTERN = re.compile(r"(___.*?___)")
MADLIBS_EDITABLE_CLASS = "madlibs-editable"
MADLIBS_EDITABLE_ICON_CLASS = "madlibs-editable-icon"
# source from Font Awesome here:
# https://fontawesome.com/icons/pen?f=classic&s=solid
SVG_PATH = "M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"  # noqa: E501


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
        element (PageElement): The element to update to an editable content.
        substring (str): The input name / placeholder input.

    Returns:
        The updated PageElement to be added to a BeautifulSoup.
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


def add_pen_svg_to_madlibs_element(
    soup: BeautifulSoup,
    element: PageElement,
) -> PageElement:
    """Adds a pen icon as an SVG Tag to the madlibs HTML content.

    Args:
        soup (BeautifulSoup): The HTML parsed soup to add the new Tags to.
        element (PageElement): The element to add an icon to.

    Returns:
        The updated PageElement to be added to a BeautifulSoup.
    """
    svg = soup.new_tag(
        name="svg",
        xmlns="http://www.w3.org/2000/svg",
        viewBox="0 0 512 512",
        **{"class": MADLIBS_EDITABLE_ICON_CLASS},
    )
    svg_path = soup.new_tag(
        name="path",
        d=SVG_PATH,
    )
    svg.append(svg_path)
    element.append(svg)

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
                    new_span = add_pen_svg_to_madlibs_element(soup, new_span)
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
                    duplicated_span = add_pen_svg_to_madlibs_element(
                        soup, duplicated_span
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
