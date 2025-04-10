# NFe Reader
#### Description:
This NF-e (Brazilian Electronic Invoice) XML Reader is a Python-based application designed to extract, format, and analyze key data from standardized NF-e XML files. 
This tool provides a Textual-based TUI (Terminal User Interface) for parsing tax documents, transforming raw XML data into structured business information, and exporting it to CSV for further analysis.

Key Features:
    1. XML Processing & Validation
        File Validation: Checks for correct .xml extension and valid NF-e structure
        Namespace Handling: Properly processes the official Brazilian NF-e XML schema (http://www.portalfiscal.inf.br/nfe)
        Error Handling: Provides clear error messages for missing files or invalid formats
    2. Data Extraction & Structuring
        The parser extracts critical invoice data, including:
            Document Information: UF (state), invoice number, emission date
            Participant Details: Emitter (CNPJ), recipient (CPF)
            Product Data: Description, quantity, unit price, total value
            Fiscal Values: ICMS taxes, total invoice amount
    3. Data Transformation & Formatting
        Date Formatting: Converts YYYY-MM-DD to Brazilian standard DD/MM/YYYY
        Tax ID Formatting: Formats CNPJ/CPF numbers (e.g., XX.XXX.XXX/XXXX-XX)
        Currency Conversion: Displays values in R$XX,XX format
        State Code Mapping: Translates IBGE codes to UF abbreviations (e.g., 35 → SP)
    4. CSV Export & DataFrame Integration
        Generates CSV files with extracted data for Excel/Google Sheets
        Uses Pandas to display structured tables in the TUI
    5. Interactive TUI with Textual
        User-Friendly Interface: Input-based navigation with real-time feedback
        Data Visualization: Pandas DataFrameTable for clean tabular display

Technical Implementation
Core Python Concepts Used:
    File I/O (XML parsing, CSV writing)
    Regular Expressions (input validation)
    Data Structures (dictionaries for structured data)
    Error Handling (try/except blocks)
    Textual Framework (interactive TUI)
    Pandas Integration (DataFrame manipulation)

Dependencies:
    xml.etree.ElementTree (XML parsing)
    csv (CSV export)
    pandas (data analysis)
    textual (terminal UI)
    textual-pandas (DataFrame display)

How to Use:
    Run python project.py
    Enter the NF-e XML filename when prompted
    View parsed data in the TUI
    Access exported CSV for further analysis

This NF-e XML Processor serves as both a practical business tool and a comprehensive demonstration of Python programming skills gained in CS50P.
