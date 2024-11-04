from django.urls import path
from .views import (
    FileUploadAPIView,
    InvoiceDetailAPIView,
    InvoiceListAPIView,
    FileDownloadAPIView,
)


urlpatterns = [
    path("upload/", FileUploadAPIView.as_view(), name="upload-invoice-file"),
    path("invoices/", InvoiceListAPIView.as_view(), name="invoice-list"),
    path("invoice/<int:pk>/", InvoiceDetailAPIView.as_view(), name="invoice-detail"),
    path(
        "download/invoice/<int:pk>/",
        FileDownloadAPIView.as_view(),
        name="invoice-download",
    ),
]
