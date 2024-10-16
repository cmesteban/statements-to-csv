# Credit Card Statement (PDF) to CSV App

This Python application processes a credit card statement in PDF format, extracts relevant information, and converts it into a CSV file. It uses the OpenAI API to format the data into two tables: an account summary and a list of categorized transactions.

## Features

- **PDF Parsing**: Extract text from a PDF credit card statement.
- **OpenAI Integration**: Sends the extracted text to the OpenAI API to format it into CSV.
- **CSV Output**: Generates a CSV file with an account summary and transaction table.
- **Dockerized Environment**: The app can be run in a Docker container for easy setup.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.
- [OpenAI API Key](https://platform.openai.com/signup/) for using the ChatGPT API.

## Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/credit-card-statement-csv.git
   ```
2. Build the Docker image:
   ```bash
   docker build -t pdf-to-csv-app .
   ```
3. Create a `.env` file with your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your-api-key-here
   ```
4. Add your PDF statements to the `statements` folder.

5. Run the Docker container:
   ```bash
   docker run -it --rm -v "$(pwd)":/app pdf-to-csv-app
   ```


## Environment Variables

The app uses a `.env` file to securely store the OpenAI API key.

### `.env` File Format

Create a `.env` file in the project root directory with the following content:

```
OPENAI_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with your actual OpenAI API key.

## Building the Docker Image

To build the Docker image, run the following command:

```bash
docker build -t pdf-to-csv-app .
```

This command does the following:
- Names the Docker image `pdf-to-csv-app`.
- Copies the project files (including `.env`) and installs the necessary dependencies.

### Optional: Tagging the Docker Image

If you want to add a version tag to the image, you can specify it during the build process. For example:

```bash
docker build -t pdf-to-csv-app:v1.0 .
```

## Running the Docker Container

Once the image is built, you can run the application with:

```bash
docker run -it --rm pdf-to-csv-app
```

### Running with a Version Tag

If you have tagged the image with a version (e.g., `v1.0`), you can run it with:

```bash
docker run -it --rm pdf-to-csv-app:v1.0
```

### Mounting Local Directories

If you want the application to access local PDF files, use the `-v` option to mount your local directory to the container. For example:

```bash
docker run -it --rm -v /path/to/local/pdfs:/app/pdfs pdf-to-csv-app
```

This will allow the app to access PDF files from your local `/path/to/local/pdfs` directory inside the Docker container.

## How to Use the Application

When you run the container, it will prompt you for the following inputs:

1. **Path to the PDF file**: Provide the path to your PDF statement.
2. **Statement Name**: Provide a name for the statement (e.g., `CreditCard_Sept2024`). This will be used for the CSV file's name and as part of the transaction table.

### Example:

```
Enter the path to the PDF statement: /app/pdfs/credit_card_statement.pdf
Enter the statement name (e.g., CreditCard_Sept2024): CreditCard_Sept2024
```

Once the application finishes, it will create a CSV file named `CreditCard_Sept2024.csv` in the current directory.

## Verifying the Docker Image

You can list your locally available Docker images by running:

```bash
docker images
```

This will display the image name and tag (e.g., `pdf-to-csv-app` and `latest` or `v1.0`).

## Cleaning Up

The `--rm` flag in the `docker run` command ensures the container is automatically removed once the app finishes. If you'd like to manually remove containers, you can use:

```bash
docker rm <container-id>
```

To remove the image from your local system:

```bash
docker rmi pdf-to-csv-app
```

Or, if you used a tag:

```bash
docker rmi pdf-to-csv-app:v1.0
```

## Dependencies

This application uses the following Python libraries:

- `openai`: To interact with the OpenAI API.
- `pdfplumber`: To parse PDF documents.
- `python-dotenv`: To securely manage environment variables.

All dependencies are listed in the `requirements.txt` file and installed during the Docker build process.

## Troubleshooting

### Common Issues:

- **PDF Not Found**: Ensure the PDF path you provide is correct, especially when running inside a Docker container. If mounting a directory, use the correct mounted path.
- **OpenAI API Key Issues**: Make sure your `.env` file is correctly formatted and accessible within the Docker container.
- **Docker Build Errors**: Ensure Docker is installed and that you have the necessary permissions to run Docker commands.
