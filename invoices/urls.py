from django.urls import path
from .views import FileUploadAPIView, InvoiceListAPIView


urlpatterns = [
    path("upload/", FileUploadAPIView.as_view(), name="upload-invoice-file"),
    path("invoices/", InvoiceListAPIView.as_view(), name="invoice-list"),
]
