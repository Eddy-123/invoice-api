from django.urls import path
from .views import (
    FileDownloadAPIView,
    FileUploadAPIView,
    InvoiceDeleteAPIView,
    InvoiceDetailAPIView,
    InvoiceListAPIView,
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
    path(
        "invoices/<int:pk>/delete/",
        InvoiceDeleteAPIView.as_view(),
        name="invoice-delete",
    ),
]
