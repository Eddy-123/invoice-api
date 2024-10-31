from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Invoice, Article
from .validators import InvoiceValidator
from .helpers import generate_excel_file


class InvoiceModelTest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            invoice_number="INV001",
            client_name="Eddy ADEGNANDJOU",
            client_email="eddy@adegnandjou.com",
            total_amount=100.00,
        )
        self.invoice_without_number = Invoice.objects.create(
            client_name="Eddy ADEGNANDJOU",
            client_email="eddy@adegnandjou.com",
            total_amount=100.00,
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.invoice_number, "INV001")
        self.assertEqual(self.invoice.client_name, "Eddy ADEGNANDJOU")
        self.assertEqual(self.invoice.client_email, "eddy@adegnandjou.com")
        self.assertEqual(self.invoice.total_amount, 100.00)
        self.assertIsNotNone(self.invoice_without_number.invoice_number)
        self.assertNotEqual(self.invoice_without_number.invoice_number, "nan")


class InvoiceListAPITest(TestCase):
    def setUp(self):
        self.invoice1 = Invoice.objects.create(
            invoice_number="INV001",
            client_name="Customer A",
            client_email="customera@example.com",
            total_amount=100.00,
        )
        self.invoice2 = Invoice.objects.create(
            invoice_number="INV002",
            client_name="Customer B",
            client_email="customerb@example.com",
            total_amount=100.00,
        )

        Article.objects.create(
            invoice=self.invoice1,
            description="Article 1",
            quantity=2,
            unit_price=25.00,
            total_price=50.00,
        )
        Article.objects.create(
            invoice=self.invoice1,
            description="Article 2",
            quantity=1,
            unit_price=50.00,
            total_price=50.00,
        )

        Article.objects.create(
            invoice=self.invoice2,
            description="Article 3",
            quantity=4,
            unit_price=50.00,
            total_price=200.00,
        )

        self.url = reverse("invoice-list")

    def test_invoice_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]["invoice_number"], "INV001")
        self.assertEqual(response.data[0]["client_name"], "Customer A")
        self.assertEqual(response.data[0]["client_email"], "customera@example.com")
        self.assertEqual(response.data[0]["total_amount"], "100.00")


class InvoiceDetailAPITest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            invoice_number="INV001",
            client_name="Customer A",
            client_email="customera@example.com",
            total_amount=100.00,
        )

        Article.objects.create(
            invoice=self.invoice,
            description="Article 1",
            quantity=2,
            unit_price=25.00,
            total_price=50.00,
        )
        Article.objects.create(
            invoice=self.invoice,
            description="Article 2",
            quantity=1,
            unit_price=50.00,
            total_price=50.00,
        )

        self.url = reverse("invoice-detail", args=[self.invoice.id])

    def test_invoice_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["invoice_number"], "INV001")
        self.assertEqual(response.data["client_name"], "Customer A")
        self.assertEqual(response.data["client_email"], "customera@example.com")
        self.assertEqual(response.data["total_amount"], "100.00")

        self.assertEqual(len(response.data["articles"]), 2)
        self.assertEqual(response.data["articles"][0]["description"], "Article 1")
        self.assertEqual(response.data["articles"][0]["quantity"], "2")
        self.assertEqual(response.data["articles"][0]["unit_price"], "25.00")
        self.assertEqual(response.data["articles"][0]["total_price"], "50.00")


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

        excel_file = generate_excel_file(data)
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
        excel_file = generate_excel_file(data)
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
        excel_file = generate_excel_file(data)
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
        excel_file = generate_excel_file(data)
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


class FileUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("upload-invoice-file")

    def test_successful_file_upload(self):
        data = [
            {
                "Numéro de facture": "INV001",
                "Nom du client": "Eddy ADEGNANDJOU",
                "Email du client": "eddy@adegnandjou.com",
                "Description de l'article": "Article A",
                "Quantité d'article": 2,
                "Prix de l'article": 50.00,
            }
        ]
        excel_file = generate_excel_file(data)
        file = SimpleUploadedFile(
            "invoices.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = self.client.post(self.url, {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["detail"], "Fichier validé et traité avec succès"
        )
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Article.objects.count(), 1)

    def test_upload_missing_file(self):
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["file"][0], "No file was submitted.")

    def test_invalid_excel_file(self):
        # Missing email
        data = [
            {
                "Numéro de facture": "INV001",
                "Nom du client": "Eddy ADEGNANDJOU",
                "Description de l'article": "Article A",
                "Quantité d'article": 2,
                "Prix de l'article": 50.00,
            }
        ]
        excel_file = generate_excel_file(data)
        file = SimpleUploadedFile(
            "invoices.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = self.client.post(self.url, {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Colonnes manquantes", response.data["detail"])
