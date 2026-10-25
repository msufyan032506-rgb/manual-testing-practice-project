# Manual Testing Practice Shop (Flask + HTML + CSS)

A small local demo e-commerce website for learning SQA manual testing. It includes product search/filtering, login, cart, quantity updates, checkout form validation, order confirmation, and contact form validation.

## Requirements
- Python 3.10+ recommended
- VS Code (optional)

## Run on Windows
1. Extract the ZIP.
2. Open the `manual_testing_practice_project` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
5. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal:
   ```cmd
   .venv\Scripts\activate.bat
   ```
6. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
7. Start the website:
   ```powershell
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.

## Demo login
- Email: `tester@example.com`
- Password: `Test123!`

These are demo-only credentials. Do not use real passwords or personal information.

## Important
- This is a local learning project, not a production store.
- No real payment is processed.
- Contact messages and orders are not saved to a database.
- `debug=True` is for local practice only. Do not deploy this project publicly.

## Suggested testing areas
- Home page and navigation
- Product search and price filters
- Login positive and negative cases
- Add to cart, multiple products, and quantity updates
- Checkout required-field validation
- Contact form validation
- Page refresh and session behaviour
- Mobile/responsive layout
- Direct URL access and empty-cart behaviour
