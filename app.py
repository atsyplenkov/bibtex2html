from shiny import App, render, ui, reactive
from shiny.types import FileInfo
from utils.bibtex_functions import *
from utils.reference_parsing import batch_ask_gpt
import faicons as fa

ICONS = {
    "html": fa.icon_svg("file-code", "regular"),
    "bookmark": fa.icon_svg("book-bookmark"),
    "python": fa.icon_svg("python"),
    "github": fa.icon_svg("github"),
}

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Plain Text",
        ui.page_fillable(
            ui.layout_columns(
                ui.card(
                    ui.card_header("Reference list"),
                    ui.input_text_area(
                        "text_input",
                        "Paste your text:",
                        resize="vertical",
                        height="300px",
                        width="100%",
                    ),
                    ui.input_action_button("run_btn", "Convert 🚀"),
                    min_height="300px",
                ),
                ui.card(
                    ui.card_header("HTML output"),
                    ui.output_ui("text_output"),
                    ui.download_button(
                        "download_bib", "Download BibTeX", icon=ICONS["bookmark"]
                    ),
                    ui.download_button(
                        "download_html", "Download HTML", icon=ICONS["html"]
                    ),
                ),
                fill=True,
                min_height="300px",
                col_widths={"sm": (5, 7)},
                gap="5px",
            )
        ),
    ),
    ui.nav_panel(
        "Upload BibTeX",
        ui.page_fillable(
            ui.layout_columns(
                ui.card(
                    ui.card_header("Upload your BibTeX file"),
                    ui.input_file("file1", "", accept=[".bib"], multiple=False),
                    ui.input_action_button("run_btn2", "Convert 🚀"),
                ),
                ui.card(
                    ui.card_header("HTML output"),
                    ui.output_ui("text_output2"),
                    ui.download_button(
                        "download_html2", "Download HTML", icon=ICONS["html"]
                    ),
                ),
                col_widths={"sm": (5, 7)},
                gap="5px",
            )
        ),
    ),
    ui.nav_panel("About", ui.markdown(open("About.md", encoding="utf-8").read())),
    ui.nav_spacer(),
    ui.nav_control(ui.input_dark_mode(mode="light")),
    title="References to BibTeX/HTML converter",
    footer=ui.tags.p(
        "Made by Anatoly Tsyplenkov using ",
        ui.tags.i(ICONS["python"]),  # Python icon
        " and ",
        ui.tags.a("Shiny", href="https://shiny.posit.co/py/"),
        ". See source code at ",
        ui.tags.a(ICONS["github"], href="https://github.com/atsyplenkov/bibtex2html"),
        style="font-size: 12px; text-align: right; padding: 10px; border-top: 1px solid #ddd; margin-top: 20px;",
    ),
)


def server(input, output, session):

    # Page 1
    @render.ui
    @reactive.event(input.run_btn)  # Trigger only when Run button is pressed
    def text_output():
        with ui.Progress(min=1, max=15) as p:
            p.set(1, message="Processing...")
            gpt_bib = batch_ask_gpt(input.text_input())
            with open("output/result.bib", "w", encoding="utf-8") as bibfile:
                bibfile.write(gpt_bib)

            bibliography = read_bib_file("output/result.bib")
            bibliography_html = bib_to_html(bibliography)
            html_to_return = "<p>" + " ".join(bibliography_html) + "</p>"
            with open("output/result", "w", encoding="utf-8") as htmlfile:
                htmlfile.write(html_to_return)

            p.set(15, message="Finished!")

        return ui.HTML(html_to_return)

    @render.download(filename="references.bib")
    def download_bib():
        return "output/result.bib"

    @render.download(filename="references.html")
    def download_html():
        return "output/result"

    # Page 2
    @render.ui
    @reactive.event(input.run_btn2)  # Trigger only when Run button is pressed
    def text_output2():
        with ui.Progress(min=1, max=15) as p:
            p.set(1, message="Processing...")
            file: list[FileInfo] | None = input.file1()
            bibliography2 = read_bib_file(file[0]["datapath"])
            bibliography_html2 = bib_to_html(bibliography2)
            html_to_return2 = "<p>" + " ".join(bibliography_html2) + "</p>"
            with open("output/result2", "w", encoding="utf-8") as htmlfile:
                htmlfile.write(html_to_return2)
            p.set(15, message="Finished!")

        return ui.HTML(html_to_return2)

    @render.download(filename="references.html")
    def download_html2():
        return "output/result2"


app = App(app_ui, server, debug=True)
