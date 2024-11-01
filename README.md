# invoice-api

This is a Django-based API designed for invoice generation as part of the Kudizy interview process

# Environment & Setup

- Python version: 3.11.9
- Clone the project:

```bash
git clone git@github.com:Eddy-123/invoice-api.git
cd invoice-api
```

- Create a virtual environment and activate the virtual environment:

```bash
python -m venv .invoice
source .invoice/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Configure environment variables

```bash
cp .env.example .env
```

- Adapt the environment variables to your local settings

- Run the tests from the root folder of the project

```bash
pytest
```

- Run the backend

```bash
python manage.py runserver
```

- The backend should be running at http://127.0.0.1:8000/

# Development process

- For each new feature, a TDD approach is adopted
- The branch feature/feature-name is used to write the code dedicated to feature-name
- The branch test/feature-name is used to write the tests dedicated to feature-name
- Both the test branch and the feature branch are merged in develop to test the feature

# Business considerations

- If an invoice number is empty in the file, a new invoice is created for this specific article
- If specified, an invoice number should take the following into consideration
  - An empty invoice number is converted to 'nan' in the database
  - A 'nan' invoice number is converted to 'nan' in the database
  - In order to avoid misconception related to the two precedent cases, a suitable invoice number format should be adopted by the business

# API Documentation

- The swagger documentation is available at: `http://127.0.0.1:8000/api/schema/swagger-ui/`

# Example of excel and csv files

- An example of the format of csv and excel files are included at invoices/files/
