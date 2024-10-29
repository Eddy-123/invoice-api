# invoice-api

This is a Django-based API designed for invoice generation as part of the Kudizy interview process

# Environment

- Python version: 3.11.9
- create a virtual environment: `python -m venv .invoice`
- activate the virtual environment: `source .invoice/bin/activate`
- install dependencies: `pip install -r requirements.txt`

# Development process

- For each new feature, a TDD approach is adopted
- The app is firstly created on the feature branch. After merging the newly created app on the test branch, the tests are written, triggering a TDD process
