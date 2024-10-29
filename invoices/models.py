from django.db import models


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture: {self.invoice_number}"


class Article(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="articles", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description
