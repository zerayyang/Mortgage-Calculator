# Mortgage Calculator

A simple mortgage calculator that extracts information from uploaded PDF applications, calculates mortgage payments and affordability ratios, and generates client reports, utilizing an LLM to support several steps in the workflow.

Built with Node.js, Python, and a web interface to simplify reviewing mortgage applications.

## Features

- Extract mortgage details from PDF applications, including supporting evidence and confidence scores.
- Review and correct extracted information before calculating.
- Calculate mortgage payments, loan-to-value (LTV), gross debt service (GDS), and total debt service (TDS).
- Generate an amortization schedule and stress-test calculations.
- Generate AI-assisted mortgage analysis.
- Open client reports and save them as PDFs using the browser’s print dialog.
- Reopen saved client reports in the same browser.

## How It Works

1. The user uploads a mortgage application PDF.
2. PyMuPDF extracts the document’s text.
3. An LLM converts the text into structured mortgage fields. If no readable text is available, the app attempts an AI PDF fallback.
4. The user reviews and corrects the extracted values.
5. Python calculates the mortgage figures.
6. The AI analyst uses the verified data and calculation results to generate an analysis.
7. The browser creates a printable client report.

The mortgage calculations are performed by Python code; the LLM supports extraction and analysis.

## Requirements

- Node.js and npm
- Python 3.10 or newer, available as `python3`
- An OpenAI API key with access to the model configured in the Python files
- An internet connection for AI features

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/zerayyang/Mortgage-Calculator.git
cd Mortgage-Calculator
```

### 2. Install Node.js dependencies

```bash
npm install
```

### 3. Set up Python

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install openai python-dotenv pydantic pymupdf
```

Keep this environment activated when starting the server so it uses the correct Python dependencies.

The separate Streamlit prototype in `Backend/app.py` also requires `streamlit`. It is not needed for the main Node.js web app.

### 4. Configure your API key

Create a file named `.env` in the project’s main folder, alongside `server.js`:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Use your own API key and keep `.env` out of Git. OpenAI API usage may incur charges.

The model is configured in:

- `Backend/ai_extractor.py`
- `Backend/ai_analyst.py`
- `Backend/pdf_fallback.py`

If a model is unavailable to your account, update those files to use an accessible model compatible with the structured-output and tool-calling features used by the app.

### 5. Start the app

```bash
node server.js
```

Open **http://localhost:3000** in your browser.

Keep the terminal running while using the app. Press **Ctrl+C** to stop it.

## Using the App

1. Upload a mortgage application PDF.
2. Review the extracted information and correct any mistakes.
3. Select **Verify & Calculate**.
4. Generate the mortgage analysis.
5. Open the client report and choose **Save as PDF** in the print dialog.

Allow browser pop-ups if the report window does not open.

## Project Structure

```text
Mortgage-Calculator/
├── Backend/
│   ├── agents/           # Extraction and analysis instructions
│   └── *.py              # PDF processing, calculations, and AI analysis
├── Samples/              # Sample documents for testing
├── Tests/                # Interactive test scripts
├── public/               # Web interface
├── uploads/              # Temporary uploads, ignored by Git
├── server.js             # Express server
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

## Sample Documents

Use the fictional PDFs in `Samples/` to try the application.

The realistic sample contains straightforward mortgage information. The confusing sample includes revised figures, different payment periods, and unverified future plans to test extraction and review.

## Testing

With the Python environment activated, run:

```bash
python3 Tests/test_ai.py
```

This is an interactive extraction and validation script. It uses the sample application, requires an API key, and may incur API charges.

For a manual check of the web app, upload a sample PDF, verify the extracted values, calculate the mortgage, generate analysis, and open the report.

## Data and Limitations

- AI extraction and analysis can make mistakes. Always review
