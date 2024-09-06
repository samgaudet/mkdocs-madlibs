import tempfile

from mkdocs.commands.build import build
from mkdocs.config import load_config

MKDOCS_CONFIG_FILEPATH = "tests/integration/mkdocs.yml"


def test_build_with_mkdocs_madlibs():
    """Test the documentation built with MkDocs Mad Libs"""
    with tempfile.TemporaryDirectory() as temp_dir:

        config = load_config(MKDOCS_CONFIG_FILEPATH)
        config.site_dir = temp_dir

        build(config)

        with open("tests/integration/index.html", "r") as index_html:
            expected_html = index_html.read()

        with open(f"{temp_dir}/index.html", "r") as test_index_html:
            test_html = test_index_html.read()

        assert expected_html == test_html
