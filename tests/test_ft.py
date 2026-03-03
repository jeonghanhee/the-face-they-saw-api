sample_text = """
[DETAIL]
동근형|95%|1.5

[TOTAL]
최종유사도|95%
"""

detail_section = sample_text.split("[DETAIL]")[1].split("[TOTAL]")[0].strip()
total_section = sample_text.split("[TOTAL]")[1].strip()

detail_lines = detail_section.split("\n")
total_score = total_section.split("|")[1].replace("%", "")

detail_reports = [
    (line.split("|")[0], int(line.split("|")[1].replace("%", "")), float(line.split("|")[2])) 
    for line in detail_lines
]

print(detail_reports)
print(total_score)