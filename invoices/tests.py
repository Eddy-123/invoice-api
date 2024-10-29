from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import Invoice, Article
from .validators import InvoiceValidator
from io import BytesIO
import pandas as pd


class InvoiceModelTest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            invoice_number="INV001",
            client_name="Eddy ADEGNANDJOU",
            client_email="eddy@adegnandjou.com",
            total_amount=100.00,
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.invoice_number, "INV001")
        self.assertEqual(self.invoice.client_name, "Eddy ADEGNANDJOU")
        self.assertEqual(self.invoice.client_email, "eddy@adegnandjou.com")
        self.assertEqual(self.invoice.total_amount, 100.00)


class ArticleModelTest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            invoice_number="INV001",
            client_name="Eddy ADEGNANDJOU",
            client_email="eddy@adegnandjou.com",
            total_amount=100.00,
        )
        self.article = Article.objects.create(
            invoice=self.invoice,
            description="Article A",
            quantity=2,
            unit_price=50.00,
            total_price=100.00,
        )

    def test_article_creation(self):
        self.assertEqual(self.article.description, "Article A")
        self.assertEqual(self.article.quantity, 2)
        self.assertEqual(self.article.unit_price, 50.00)
        self.assertEqual(self.article.total_price, 100.00)


class InvoiceValidatorTest(TestCase):
    def generate_excel_file(self, data):
        output = BytesIO()
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return output

    def test_valid_excel_file(self):
        data = [
            {
                "Numéro de facture": "INV001",
                "Nom du client": "Eddy ADEGNANDJOU",
                "Email du client": "eddy@adegnandjou.com",
                "Description de l'article": "Article A",
                "Quantité d'article": 2,
                "Prix de l'article": 50.00,
            },
            {
                "Numéro de facture": "INV001",
                "Nom du client": "Eddy ADEGNANDJOU",
                "Email du client": "eddy@adegnandjou.com",
                "Description de l'article": "Article B",
                "Quantité d'article": 1,
                "Prix de l'article": 25.00,
            },
        ]

        excel_file = self.generate_excel_file(data)
        file = SimpleUploadedFile(
            "test.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        validated_data = InvoiceValidator.validate_file(file)
        self.assertEqual(len(validated_data), 2)

    def test_excel_missing_columns(self):
        # Missing email column
        data = [
            {
                "Numéro de facture": "INV001",
                "Nom du client": "Eddy ADEGNANDJOU",
                "Description de l'article": "Article A",
                "Quantité d'article": 2,
                "Prix de l'article": 50.00,
            }
        ]
        excel_file = self.generate_excel_file(data)
        file = SimpleUploadedFile(
            "test.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        with self.assertRaises(ValidationError) as context:
            InvoiceValidator.validate_file(file)
        self.assertIn("Colonnes manquantes", str(context.exception))

    def test_invalid_data_type_in_excel(self):
        # Invalid quantity
        data = [
            {
                "Numéro de facture": "INV002",
                "Nom du client": "Eddy ADEGNANDJOU",
                "Email du client": "eddy@adegnandjou.com",
                "Description de l'article": "Article C",
                "Quantité d'article": "three",
                "Prix de l'article": 100.00,
            }
        ]
        excel_file = self.generate_excel_file(data)
        file = SimpleUploadedFile(
            "test.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        with self.assertRaises(ValidationError) as context:
            InvoiceValidator.validate_file(file)
        self.assertIn("Quantité", str(context.exception))

    def test_invalid_email_in_excel(self):
        data = [
            {
                "Numéro de facture": "INV003",
                "Nom du client": "Eddy ADEGNANDJOU",
                "Email du client": "invalid-email",
                "Description de l'article": "Article X",
                "Quantité d'article": 5,
                "Prix de l'article": 15.00,
            }
        ]
        excel_file = self.generate_excel_file(data)
        file = SimpleUploadedFile(
            "test.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        with self.assertRaises(ValidationError) as context:
            InvoiceValidator.validate_file(file)
        self.assertIn("Adresse e-mail invalide", str(context.exception))

    def test_valid_csv_file(self):
        content = (
            "Numéro de facture,Nom du client,Email du client,"
            "Description de l'article,Quantité d'article,Prix de l'article\n"
            "INV001,Eddy ADEGNANDJOU,eddy@adegnandjou.com,Produit A,2,50.00\n"
        ).encode("utf-8")
        file = SimpleUploadedFile("test.csv", content, content_type="text/csv")

        data = InvoiceValidator.validate_file(file)
        self.assertEqual(len(data), 1)

    def test_invalid_file_extension(self):
        file = SimpleUploadedFile(
            "test.txt", b"Invalid content", content_type="text/plain"
        )
        with self.assertRaises(ValidationError):
            InvoiceValidator.validate_file(file)
