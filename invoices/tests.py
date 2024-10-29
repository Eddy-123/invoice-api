from django.test import TestCase
from invoices.models import Invoice, Article


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
