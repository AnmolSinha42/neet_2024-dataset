from PyPDF2 import PdfReader
import pandas as pd

pd.read_table

reader = PdfReader("neet_stats.pdf")

for i in range(len(reader.pages)):
    page = reader.pages[i].extract_text()
    print(page)
    break