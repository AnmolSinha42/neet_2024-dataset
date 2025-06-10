from PyPDF2 import PdfReader #
from PyPDF2 import PdfReader #vardhman
import csv

reader = PdfReader("neet_stats.pdf")
total_pages = len(reader.pages)

content = []
true_line = ""

for i in range(total_pages):
    page = reader.pages[i].extract_text()
    page = page.replace("Admitted Candidates List All Round- MBBS/BDS/B.Sc. Nursing (UG 2024)","") #remove unnecessary text
    page_content = page.split("\n")        #make every line as a list item
    page_content = page_content[2:]        #first line was pageno and 2nd was roll no etc  

    #true line is 1 row of the dataset or pdf
    # a "true line" contains all info for a single candidate (2 lines long)
     #content is a list where each item is a true line
   
    for line in page_content:
        if line[0:10].isnumeric(): #length of a roll no is 10 and each true line starts with roll number
            #if true_line[0:10] == "2002240029" or true_line[0:10] == "2807030391": -- gives exception
            content.append(true_line) #will make 1st line empty
            true_line = line
        else:
            true_line += line
    print(f"page {i} done")

content.pop(0) #1st line is empty
content.append(true_line)

file = open("neet24.csv","w")
csv_writer = csv.writer(file)
csv_writer.writerow(["roll","quota","AIR","caste","PwD","choice","institute_code","institute","degree","alloted_category","alloted_ph","round"])

#extract candidate info from content
for line_no in range(len(content)):
    row = content[line_no]
    roll = row[0:10]
    row=row.replace(roll,"",1)
    row = row.split()
    row = " ".join(row)
    quota = ""
    i=0
    while not row[i].isnumeric():
        quota += row[i]
        i += 1
    row=row.replace(quota,"",1)
    row = row.strip()

    rank = ""
    i=0
    if row[i]==" ":
        i+=1
    while row[i].isnumeric() or row[i]==".":
        rank += row[i]
        if row[i+1]== " ":
            i+=1
        i += 1
    row=row.replace(rank,"",1)

    row = row.split()
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

    round = row[-1]
    row = row[0:-1]
    row = row.strip() 
    if "Disability" in row:
        row = row.replace("Person with Disability","")
        ph = "PwD"
    else:
        ph = row[-2:] #ph is "NO"
        row = row[0:-2]
    row = row.strip()

    row = row.split()
    row = " ".join(row)

    #only 3 subjects - MBBS, BDS, B.Sc. Nursing
    if "B.Sc. Nursing" in row:
        deg = "B.Sc. Nursing"
    elif "BDS" in row:
        deg = "BDS"
    else:
        deg = "MBBS"
    row = row[::-1]
    row=row.replace(deg[::-1],"_",1)
    cat = row.partition("_")[0][::-1]
    row = row[::-1]

    row = row.replace(cat,"")
    row = row.replace("_","")
    inst = row

    data = [roll,quota,rank,caste,sub_cat,choice,inst_code,inst,deg,cat, ph, round]
    csv_writer.writerow(data)
    #sql.execute("INSERT INTO neet (roll,quota,AIR,caste,PwD,choice,institute_code,institute,degree,alloted_category,alloted_ph,round) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(roll,quota,rank,caste,sub_cat,choice,inst_code,inst,deg,cat, ph, round))
        
    
    #print(roll,quota,rank,caste,sub_cat,choice,inst_code,deg,cat, ph, round)
file.close()

