import g4f
import re

with open("prompt.md", "r") as file:
    md_content = file.read()


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


def ask_gpt(prompt: str) -> str:
    """
    This function sends a prompt to GPT-3.5 Turbo and returns the response.

    Args:
        prompt (str): The prompt to be sent to GPT-3.5 Turbo.

    Returns:
        str: The plain text response from GPT-3.5 Turbo.
    """

    # Format the prompt by adding the content of the prompt.md file to it.
    formatted_prompt = f"{md_content}: {prompt} \n\n Make sure that only the plain text is returned, do not try to return this as a markdown code block."

    # Send the formatted prompt to GPT-3.5 Turbo and get the response.
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The model to be used for generating the response.
        messages=[
            {"role": "user", "content": formatted_prompt}
        ],  # The user message to be sent to the model.
    )

    # Return the response after stripping any leading or trailing whitespaces.
    return response.strip()


test = "Tsyplenkov, A. S., Golosov, V. N., & Kuksina, L. V. (2017). Assessment of basin component of suspended sediment yield generated due to rainfall events at small rivers in wet and dry subtropics. Engineering Survey, 9, 54–65. https://doi.org/10.25296/1997-8650-2017-9-54-65\nChalov, S., Golosov, V., Tsyplenkov, A., Theuring, P., Zakerinejad, R., Maerker, M., & Samokhin, M. (2017). A toolbox for sediment budget research in small catchments. GEOGRAPHY, ENVIRONMENT, SUSTAINABILITY, 10(4), 43–68. https://doi.org/10.24057/2071-9388-2017-10-4-43-68"

test_bib = ask_gpt(test)
test_bib = test_bib.replace("doi={https://doi.org/", "doi={")
print(test_bib)

with open("example.bib", "w") as bibfile:
    bibfile.write(test_bib)


from citeproc.source.bibtex import BibTeX
from citeproc import CitationStylesStyle, CitationStylesBibliography, formatter
from citeproc_styles import get_style_filepath
from citeproc import Citation, CitationItem

# Load BibTeX file
bib_src = BibTeX("example.bib", encoding="utf-8")

# Load CSL file — name can be anything that has a .csl file in the repo
stylepath = get_style_filepath("apa")
bib_style = CitationStylesStyle(stylepath, validate=False)

# Instantiate library
bibliography = CitationStylesBibliography(bib_style, bib_src, formatter.html)

for i in bib_src:
    bibliography.register(Citation([CitationItem(i)]))

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


ready_bib = bib_to_html(bibliography.bibliography())
print(ready_bib)

# Write bibliography
with open("example.html", "w", encoding="utf-8") as htmlfile:
    for i, x in enumerate(ready_bib):
        htmlfile.write(x)
