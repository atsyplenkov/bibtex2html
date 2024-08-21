from utils.bibtex_functions import *
from utils.reference_parsing import batch_ask_gpt

test = "Bibentyo, T. M., Dille, A., Depicker, A., Smets, B., Vanmaercke, M., Nzolang, C., Dewaele, S., & Dewitte, O. (2024). Landslides, bedrock incision and human-induced environmental changes in an extremely rapidly formed tropical river gorge. Geomorphology, 109046. https://doi.org/10.1016/j.geomorph.2023.109046\nChen, M., Tang, C., Chang, M., & Xiong, J. (2024). Seismically induced hillslope disturbance, sediment connectivity and mass wasting: Insights from the 2008 Wenchuan earthquake. Geomorphology, 449, 109064. https://doi.org/10.1016/j.geomorph.2024.109064\nMcColl, S. T., & Cook, S. J. (2024). A universal size classification system for landslides. Landslides, 21(1), 111–120. https://doi.org/10.1007/s10346-023-02131-6\nPitscheider, F., Steger, S., Cavalli, M., Comiti, F., & Scorpio, V. (2024). Areas simultaneously susceptible and (dis-)connected to debris flows in the Dolomites (Italy): Regional-scale application of a novel data-driven approach. Journal of Maps, 20(1), 1–14. https://doi.org/10.1080/17445647.2024.2307549"

# gpt_bib = ask_gpt(test)
# with open("output/result.bib", "w", encoding="utf-8") as bibfile:
#     bibfile.write(gpt_bib)

# bibliography = read_bib_file("output/result.bib")
# bibliography_html = bib_to_html(bibliography)

# "<p>" + " ".join(bibliography_html) + "</p>"


# Split the string into a list
test_list = test.split("\n")
my_list = [element + "\n" for element in test_list]
result = ["\n".join(my_list[i : i + 3]) for i in range(0, len(my_list), 3)]

# Run gpt task
outcome = []
for i, x in enumerate(result):
    outcome.append(ask_gpt(str(x)))

# Write GPT response
outcome2 = [element.strip() + "\n\n" for element in outcome]
outcome2 = "".join(outcome2)
with open("output/result.bib", "w", encoding="utf-8") as bibfile:
    bibfile.write(outcome2)

# Read bibliography
bibliography = read_bib_file("output/result.bib")
bibliography_html = bib_to_html(bibliography)
"<p>" + " ".join(bibliography_html) + "</p>"

outcome2 = batch_ask_gpt(test)



####
b = read_bib_file("data\citations_bib.bib")
bib_to_html(b)
