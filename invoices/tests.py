from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import Invoice, Article
from .validators import InvoiceValidator


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
