from PyPDF2 import PdfReader

reader = PdfReader("neet_stats.pdf")
total_pages = len(reader.pages)

content = []
for i in range(100):
    page = reader.pages[i].extract_text()
    page = page.replace("Admitted Candidates List All Round- MBBS/BDS/B.Sc. Nursing (UG 2024)","") #remove unnecessary text
    page_content = page.split("\n")        #make every line as a list item
    page_content = page_content[2:]        #first line was pageno and 2nd was roll no etc  

    #true line is 1 row of the dataset or pdf
    # a "true line" contains all info for a single candidate (2 lines long)
     #content is a list where each item is a true line
    true_line = ""
    for line in page_content:
        if line[0].isdigit() and len(line.split()[0])==10: #length of a roll no is 10 and each true line starts with roll number
            content.append(true_line)
            true_line = line
        else:
            true_line += line
    content.append(true_line)
    print(f"page {i} done")

print()
print("\n\n".join(content))

    
