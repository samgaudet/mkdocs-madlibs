import pytest
from bs4 import BeautifulSoup

from mkdocs_madlibs._fence import fence

BASIC_HTML_DOCUMENT = """
<!DOCTYPE html>
<html>
<body>
</body>
</html>
"""

BASIC_TAG_STRING = "___NAME___"

BASIC_CODE_BLOCK_MARKDOWN__UNDERSCORES = """
python
~~~
print("Hello, ___NAME___.")
"""
BASIC_CODE_BLOCK_MARKDOWN__CARETS = """
python
~~~
print("Hello, ^^^NAME^^^.")
"""

BASIC_CODE_BLOCK_HTML = """
  <div class="language-python.highlight highlight">
   <pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"Hello, </span><span class="madlibs-editable" contenteditable="true" onclick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit NAME">NAME<svg class="madlibs-editable-icon" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span><span class="s2">."</span><span class="p">)</span>
</code></pre>
  </div>
"""

MULTI_INPUT_CODE_BLOCK_MARKDOWN = """
terraform
~~~
resource "google_project_iam_member" "project" {
  project = "___PROJECT_ID___"
  role    = "roles/___ROLE___"
  member  = "user:___EMAIL___"
}
"""
MULTI_INPUT_CODE_BLOCK_HTML = """
<div class="language-terraform.highlight highlight">
 <pre><span></span><code><span class="kr">resource</span><span class="w"> </span><span class="nc">"google_project_iam_member"</span><span class="w"> </span><span class="nv">"project"</span><span class="w"> </span><span class="p">{</span>
<span class="w">  </span><span class="na">project</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="s2">"</span><span class="madlibs-editable" contenteditable="true" onClick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit PROJECT_ID">PROJECT_ID<svg class="madlibs-editable-icon" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span><span class="s2">"</span>
<span class="w">  </span><span class="na">role</span><span class="w">    </span><span class="o">=</span><span class="w"> </span><span class="s2">"roles/</span><span class="madlibs-editable" contenteditable="true" onClick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit ROLE">ROLE<svg class="madlibs-editable-icon" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span><span class="s2">"</span>
<span class="w">  </span><span class="na">member</span><span class="w">  </span><span class="o">=</span><span class="w"> </span><span class="s2">"user:</span><span class="madlibs-editable" contenteditable="true" onClick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit EMAIL">EMAIL<svg class="madlibs-editable-icon" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span><span class="s2">"</span>
<span class="p">}</span>
</code></pre>
</div>
"""

PLAIN_TEXT_CODE_BLOCK_MARKDOWN = """
text
~~~
"___EXCLAMATION___!" he said ___ADVERB___ as he jumped into his convertible ___NOUN___ and drove off with his ___ADJECTIVE___ wife.
"""
PLAIN_TEXT_CODE_BLOCK_HTML = """
<div class="language-text.highlight highlight">
<pre><span></span><code>"<span class="madlibs-editable" contenteditable="true" onclick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit EXCLAMATION">EXCLAMATION<svg class="madlibs-editable-icon" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span>!" he said <span class="madlibs-editable" contenteditable="true" onclick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit ADVERB">ADVERB<svg class="madlibs-editable-icon" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span> as he jumped into his convertible <span class="madlibs-editable" contenteditable="true" onclick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit NOUN">NOUN<svg class="madlibs-editable-icon" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span> and drove off with his <span class="madlibs-editable" contenteditable="true" onclick="document.execCommand('selectAll',false,null)" spellcheck="false" title="Edit ADJECTIVE">ADJECTIVE<svg class="madlibs-editable-icon" viewbox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z"></path></svg></span> wife.
</code></pre>
</div>
"""


@pytest.mark.parametrize(
    argnames=["test_markdown", "test_html"],
    argvalues=[
        (BASIC_CODE_BLOCK_MARKDOWN__UNDERSCORES, BASIC_CODE_BLOCK_HTML),
        (BASIC_CODE_BLOCK_MARKDOWN__CARETS, BASIC_CODE_BLOCK_HTML),
        (MULTI_INPUT_CODE_BLOCK_MARKDOWN, MULTI_INPUT_CODE_BLOCK_HTML),
        (PLAIN_TEXT_CODE_BLOCK_MARKDOWN, PLAIN_TEXT_CODE_BLOCK_HTML),
    ],
)
def test_fence(test_markdown: str, test_html: str):
    """Test the fence functionality and ensure the rendered HTML is valid."""
    html = fence(
        source=test_markdown,
        # the following arguments are not really used
        # we can pad them for testing
        language=None,
        css_class=None,
        options=None,
        md=None,
    )

    expected_html = BeautifulSoup(BASIC_HTML_DOCUMENT, "html.parser")
    generated_html = BeautifulSoup(BASIC_HTML_DOCUMENT, "html.parser")
    expected_html.body.append(BeautifulSoup(test_html, "html.parser"))  # type: ignore
    generated_html.body.append(BeautifulSoup(html, "html.parser"))  # type: ignore

    assert expected_html.prettify() == generated_html.prettify()
