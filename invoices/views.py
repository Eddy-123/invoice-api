from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import pandas as pd
from .models import Invoice, Article
from decimal import Decimal


class FileUploadViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]

    def create(self, request):
        file = request.FILES["file"]

        if file.name.endswith(".xlsx"):
            data = pd.read_excel(file)
        else:
            data = pd.read_csv(file)

        for _, row in data.iterrows():
            invoice = None
            invoice_number = row.get("Numéro de facture", None)
            description = row["Description de l'article"]
            quantity = row["Quantité d'article"]
            unit_price = row["Prix de l'article"]

            if invoice_number is not None:
                if Invoice.objects.filter(invoice_number=invoice_number).exists():
                    invoice = Invoice.objects.get(invoice_number=invoice_number)

            if invoice is None:
                invoice = Invoice.objects.create(
                    invoice_number=row.get("Numéro de facture", None),
                    client_name=row["Nom du client"],
                    client_email=row["Email du client"],
                    total_amount=0,
                )

            article = Article.objects.create(
                invoice=invoice,
                description=description,
                quantity=quantity,
                unit_price=unit_price,
                total_price=Decimal(quantity * unit_price),
            )

            invoice.total_amount += article.total_price
            invoice.save()

        return Response(status=status.HTTP_201_CREATED)
