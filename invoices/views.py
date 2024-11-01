from django.core.exceptions import ValidationError
from decimal import Decimal
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from .validators import InvoiceValidator
from .models import Invoice, Article
from .serializers import FileSerializer, InvoiceListSerializer, InvoiceSerializer


class FileUploadAPIView(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        operation_id="uploadFile",
        summary="Upload a file",
        description="Uploads a file to the server and returns a success message",
        request=FileSerializer,
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Success Response",
                        summary="File uploaded successfully",
                        value={"detail": "Fichier validé et traité avec succès"},
                    )
                ],
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Validation Error",
                        summary="File is required or invalid",
                        value={"file": ["No file was submitted."]},
                    )
                ],
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES["file"]

        if not file:
            return Response(
                {"detail": "Aucun fichier fourni"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data = InvoiceValidator.validate_file(file)

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

            return Response(
                {"detail": "Fichier validé et traité avec succès"},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InvoiceListAPIView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceListSerializer


class InvoiceDetailAPIView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
