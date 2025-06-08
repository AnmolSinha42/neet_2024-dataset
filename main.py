from PyPDF2 import PdfReader

reader = PdfReader("neet_stats.pdf")
total_pages = len(reader.pages)

content = []
true_line = ""
for i in range(20):
    page = reader.pages[i].extract_text()
    page = page.replace("Admitted Candidates List All Round- MBBS/BDS/B.Sc. Nursing (UG 2024)","") #remove unnecessary text
    page_content = page.split("\n")        #make every line as a list item
    page_content = page_content[2:]        #first line was pageno and 2nd was roll no etc  

    #true line is 1 row of the dataset or pdf
    # a "true line" contains all info for a single candidate (2 lines long)
     #content is a list where each item is a true line
   
    for line in page_content:
        if line.split()[0].isnumeric() and len(line.split()[0])==10: #length of a roll no is 10 and each true line starts with roll number
            content.append(true_line) #will make 1st line empty
            true_line = line
        else:
            true_line += line
    print(f"page {i} done")

content.pop(0) #1st line is empty
content.append(true_line)

#extract candidate info from content
for line_no in range(len(content)):
    row = content[line_no].split()
    cat, ph, round = row[-3:] #all are strings, cat is alloted category
    del row[-3:]
    roll = row.pop(0)

    row = " ".join(row)
    quota = ""
    i=0
    while not row[i].isnumeric():
        quota += row[i]
        i += 1
    row=row.replace(quota,"",1)

    row = row.split()
    rank = row.pop(0)
    caste = row.pop(0)
    sub_cat = row.pop(0) #pwd etc
    choice = row.pop(0) #option number in priority list

    row = " ".join(row)
    inst_code = ""
    i=0
    while row[i].isnumeric():
        inst_code += row[i]
        i += 1
    row=row.replace(inst_code,"",1)

    #only 3 subjects - MBBS, BDS, B.Sc. Nursing
    if row[-4:]=="MBBS":
        deg = "MBBS"
    elif row[-3:]=="BDS":
        deg = "BDS"
    else:
        deg = "B.Sc. Nursing"
    row = row[::-1]
    row=row.replace(deg[::-1],"",1)
    row = row[::-1]
    
    inst = row

        

    print(roll,quota,rank,caste,sub_cat,choice,inst_code,deg,cat, ph, round)



