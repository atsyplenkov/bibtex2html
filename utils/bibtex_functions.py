import re
from citeproc.source.bibtex import BibTeX
from citeproc import CitationStylesStyle, CitationStylesBibliography, formatter
from citeproc_styles import get_style_filepath
from citeproc import Citation, CitationItem


def read_bib_file(file: str) -> list:
    """
    Read a BibTeX file and convert it to a list of bibliography items.
    """
    # Load BibTeX file
    bib_file = BibTeX(file, encoding="utf-8")

    # Load CSL style
    style_path = get_style_filepath("apa")
    style = CitationStylesStyle(style_path, validate=False)

    # Create bibliography
    bibliography = CitationStylesBibliography(style, bib_file, formatter.html)

    # Register all items in the bibliography
    for item in bib_file:
        bibliography.register(Citation([CitationItem(item)]))

    # Return the bibliography
    return bibliography.bibliography()


def bib_to_html(bibliography) -> list:
    """
    Convert a bibliography to a list of HTML strings.
    """
    html_bibliography = []
    for item in bibliography:
        html_item = add_hyperlinks(str(item))
        html_item = html_item.replace("..", ".")
        html_item = html_item.replace(",,", ",")
        html_bibliography.append(html_item)
    html_bibliography.sort()
    return html_bibliography


def add_hyperlinks(text: str) -> str:
    """
    Add HTML hyperlinks to all URLs in the given text.

    Args:
        text (str): The text containing URLs to be converted to hyperlinks.

    Returns:
        str: The text with URLs converted to hyperlinks.
    """
    # Regular expression pattern to match URLs
    pattern = r"(https?://\S+)"

    # Function to replace URLs with HTML hyperlinks and add a line break
    def replace_url(match):
        """
        Replace a URL with an HTML hyperlink and add a line break.
        """
        url = match.group(1)
        return f'<a href="{url}" target="_blank">{url}</a>'

    # Replace URLs with HTML hyperlinks and add line breaks
    output = re.sub(pattern, replace_url, text)
    output = output + "<br>"

    return output
