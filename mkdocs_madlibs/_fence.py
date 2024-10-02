import copy
import re
from typing import List

from bs4 import BeautifulSoup, NavigableString, Tag
from pymdownx.highlight import Highlight

MADLIBS_PATTERN = re.compile(
    r"(?P<full_match>(?P<opening_chars>___|\^\^\^).*?(?P<closing_chars>___|\^\^\^))"
)
MADLIBS_EDITABLE_CLASS = "madlibs-editable"
MADLIBS_EDITABLE_ICON_CLASS = "madlibs-editable-icon"
# source from Font Awesome here:
# https://fontawesome.com/icons/pen?f=classic&s=solid
SVG_PATH = "M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"  # noqa: E501


def prepare_madlibs_element(
    element: Tag,
    substring: str,
    match: re.Match,
) -> Tag:
    """Prepare the MkDocs Madlibs element, including
    - Strip the element's content of opening and closing characters.
    - Set the `title` to the Tag as a tooltip for users.
    - Set the CSS `class` to `madlibs-editable` to style the Tag.
    - Set the `contenteditable` attribute to `true` to allow user editing.
    - Set the `onClick` behavior to select all text when clicked.
    - Set `spellcheck` to `false` to avoid visual bugs with spelling errors.

    Args:
        element (Tag): The element to update to an editable content.
        substring (str): The input name / placeholder input.
        match (Match): The REGEX Match object.

    Returns:
        The updated Tag to be added to a BeautifulSoup.
    """
    cleaned_content = substring.replace(match["opening_chars"], "").replace(
        match["closing_chars"], ""
    )
    element.string = cleaned_content
    element["title"] = f"Edit {cleaned_content}"
    element["class"] = [MADLIBS_EDITABLE_CLASS]
    element["contenteditable"] = "true"
    # select all text on click; stolen from:
    # https://stackoverflow.com/a/3805897
    element["onClick"] = "document.execCommand('selectAll',false,null)"
    element["spellcheck"] = "false"

    return element


def add_pen_svg_to_madlibs_element(
    soup: BeautifulSoup,
    element: Tag,
) -> Tag:
    """Adds a pen icon as an SVG Tag to the madlibs HTML content.

    Args:
        soup (BeautifulSoup): The HTML parsed soup to add the new Tags to.
        element (Tag): The element to add an icon to.

    Returns:
        The updated Tag to be added to a BeautifulSoup.
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

    # appease mypy's type hinting
    # exit early if we don't parse a Tag
    if isinstance(code, NavigableString) or not code:
        return html

    for element in code.contents:
        if isinstance(element, NavigableString):
            match = MADLIBS_PATTERN.search(element)

            if not match:
                continue

            substrings = element.partition(match["full_match"])

            # iterate over the reversed list of substrings
            # so they are added 'in order' when using `insert_after`
            for substring in reversed(substrings):
                # annoyingly, we have to check for empty substrings
                if substring and substring.startswith(match["opening_chars"]):
                    new_span = soup.new_tag("span")
                    new_span = prepare_madlibs_element(new_span, substring, match)
                    new_span = add_pen_svg_to_madlibs_element(soup, new_span)
                    element.insert_after(new_span)
                elif substring:
                    new_element = NavigableString(substring)
                    element.insert_after(new_element)
                else:
                    pass

            # remove the original span that has been split
            element.extract()

        # if the span has content, check the content of the span
        elif isinstance(element, Tag) and element.name == "span" and element.string:
            match = MADLIBS_PATTERN.search(element.string)

            if not match:
                continue

            substrings = element.string.partition(match["full_match"])

            # iterate over the reversed list of substrings
            # so they are added 'in order' when using `insert_after`
            for substring in reversed(substrings):
                duplicated_span = copy.copy(element)

                if substring.startswith(match["opening_chars"]):
                    duplicated_span = prepare_madlibs_element(
                        duplicated_span, substring, match
                    )
                    duplicated_span = add_pen_svg_to_madlibs_element(
                        soup, duplicated_span
                    )
                else:
                    duplicated_span.string = substring

                element.insert_after(duplicated_span)

            # remove the original span that has been split
            element.extract()

        # if the span does not have content, search for other spans with content
        elif isinstance(element, Tag) and element.name == "span" and not element.string:
            for span in element.find_all("span"):
                match = MADLIBS_PATTERN.search(span.string)

                if not match:
                    continue

                substrings = span.string.partition(match["full_match"])

                # iterate over the reversed list of substrings
                # so they are added 'in order' when using `insert_after`
                for substring in reversed(substrings):
                    duplicated_span = copy.copy(span)

                    if substring.startswith(match["opening_chars"]):
                        duplicated_span = prepare_madlibs_element(
                            duplicated_span, substring, match
                        )
                        duplicated_span = add_pen_svg_to_madlibs_element(
                            soup, duplicated_span
                        )
                    else:
                        duplicated_span.string = substring

                    span.insert_after(duplicated_span)

                # remove the original span that has been split
                span.extract()

        else:
            pass

    modified_html = str(soup.prettify())
    return modified_html


def prepare_hl_lines(hl_lines: str, line_count: int) -> List[int]:
    """Prepare the code block lines to highlight.
    This replaces the `parse_hl_lines` function in:
    https://github.com/facelessuser/pymdown-extensions/blob/main/pymdownx/superfences.py

    Args:
        hl_lines (str): The hl_lines attribute.
        line_count (int): The number of lines in the code snippet.

    Returns:
        The line numbers to highlight, as a list of strings.
    """

    def normalize_hl_lines_range(line_index: int, line_count: int) -> int:
        """Restrict the max line number to the line_count plus one.

        Args:
            line_index (int): The line index.
            line_count (int): The total line count.

        Returns:
            The modified line index as an integer.
        """
        if line_index < 1:
            line_index = 0
        elif line_index > line_count:
            line_index = line_count + 1
        return line_index

    prepared_hl_lines: List[int] = []
    for lines in hl_lines.split():
        line_range: List[int] = [
            normalize_hl_lines_range(int(split_lines), line_count)
            for split_lines in lines.split("-")
        ]
        if len(line_range) > 1:
            if line_range[0] <= line_range[1]:
                prepared_hl_lines.extend(list(range(line_range[0], line_range[1] + 1)))
        elif 1 <= line_range[0] <= line_count:
            prepared_hl_lines.extend(line_range)

    return prepared_hl_lines


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
    title = attrs.get("title", None) if attrs else None
    hl_lines = attrs.get("hl_lines", None) if attrs else None

    if hl_lines:
        line_count = _source.count("\n") + 1
        prepared_hl_lines = prepare_hl_lines(hl_lines=hl_lines, line_count=line_count)

    highlighter = Highlight()

    code_block = highlighter.highlight(
        src=_source,
        language=_language,
        hl_lines=prepared_hl_lines if hl_lines else hl_lines,
        classes=[f"language-{_language}.highlight"],
        title=title,
    )

    modified_html = modify_code_block_html(code_block)

    return modified_html
