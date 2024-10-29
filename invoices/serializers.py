from rest_framework import serializers
from .models import Invoice, Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["description", "quantity", "unit_price", "total_price"]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "client_name",
            "client_email",
            "total_amount",
            "articles",
            "created_at",
        ]
