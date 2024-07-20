from common.config import *
from PyPDF2 import PdfReader
print(base_dir)

output_file = os.path.join(PDFstoReadFolder, "output.txt")

# Get a list of all PDF files in the folder
pdf_files = [file for file in os.listdir(PDFstoReadFolder) if file.endswith(".pdf")]

# Open the output text file in write mode
with open(file=output_file, mode="w", encoding='utf-8') as text_file:
    # Iterate over each PDF file
    for pdf_file in pdf_files:
        # Construct the full file path
        file_path = os.path.join(PDFstoReadFolder, pdf_file)
        print(f"Trying to read : {file_path}")
        
        # Open the PDF file
        with open(file_path, "rb") as pdf:
            # Create a PDF reader object
            pdf_reader = PdfReader(pdf)
            
            # Iterate over each page of the PDF
            for page in pdf_reader.pages:
                # Extract the text from the page
                text = page.extract_text()
                
                # Write the extracted text to the output file
                text_file.write(text)
                text_file.write("\n")  # Add a newline for readability

print("Text extraction completed. Output saved to", output_file)