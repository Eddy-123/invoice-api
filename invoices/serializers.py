from rest_framework import serializers
from .models import Invoice, Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["description", "quantity", "unit_price", "total_price"]


class InvoiceSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)

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


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
    name = serializers.CharField(max_length=255, required=False)

    def validate_file(self, value):
        max_file_size = 5 * 1024 * 1024
        if value.size > max_file_size:
            raise serializers.ValidationError("Taille du fichier dépasse 5MB")

        valid_mime_type = [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "text/csv",
            "application/csv",
        ]
        if value.content_type not in valid_mime_type:
            raise serializers.ValidationError(
                "Type de fichier incompatible. Types autorisés: CSV, XLSX"
            )

        return value
