import pdfplumber
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to call ChatGPT API to generate CSV
def call_chatgpt_to_generate_csv(pdf_text, statement_name):
    
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    prompt = f"""
    I have a credit card statement with the following data:

    {pdf_text}

    Please format this into a CSV file with two tables:

    Table 1: Account Summary
    Column Headers: Name, Amount
    Rows: Transactions, Fees, Interest, New Balance, Rewards Balance

    Table 2: {statement_name}
    Column Headers: Expense Name, Description, Trans Date, Post Date, Amount (USD), Category
    Category options: restaurant, groceries, entertainment, rent, gas, transportation, shopping, miscellaneous.
    Rows: Each transaction parsed from the statement.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10000,
        temperature=0
    )

    return response.choices[0].message['content'].strip()

# Main function to loop through all PDFs in the 'statements' folder
def main():
    statements_folder = './statements'  # Folder containing the PDFs
    pdf_files = [f for f in os.listdir(statements_folder) if f.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the 'statements' folder.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(statements_folder, pdf_file)
        
        # Extract text from the current PDF
        try:
            pdf_text = extract_text_from_pdf(pdf_path)
            print("PDF Text: ", pdf_text)
        except FileNotFoundError:
            print(f"Error: The PDF file '{pdf_file}' was not found.")
            continue
        except Exception as e:
            print(f"Error processing file '{pdf_file}': {e}")
            continue

        # Remove the .pdf extension to use the file name as the table name
        statement_name = os.path.splitext(pdf_file)[0]

        # Call ChatGPT to generate the CSV content
        csv_content = call_chatgpt_to_generate_csv(pdf_text, statement_name)

        # Save the CSV file with the same name as the PDF
        csv_filename = f"{statement_name}.csv"
        csv_path = os.path.join(statements_folder, csv_filename)

        with open(csv_path, 'w') as file:
            file.write(csv_content)

        print(f"CSV file '{csv_filename}' created successfully in the 'statements' folder.")

if __name__ == "__main__":
    main()