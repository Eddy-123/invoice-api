import pandas as pd
from django.core.exceptions import ValidationError


class InvoiceValidator:
    REQUIRED_COLUMNS = [
        "Numéro de facture",
        "Nom du client",
        "Email du client",
        "Description de l'article",
        "Quantité d'article",
        "Prix de l'article",
    ]

    @classmethod
    def validate_file(cls, file):
        try:
            if file.name.endswith(".xlsx"):
                data = pd.read_excel(file)
            elif file.name.endswith(".csv"):
                data = pd.read_csv(file)
            else:
                raise ValidationError("Le format de fichier doit être .csv ou .xlsx")

            cls.validate_columns(data)
            cls.validate_data_types(data)
            cls.validate_rows(data)
        except Exception as e:
            raise ValidationError(f"Erreur lors de la validation du fichier: {str(e)}")

        return data

    @classmethod
    def validate_columns(cls, data):
        missing_columns = []
        for col in cls.REQUIRED_COLUMNS:
            if col not in data.columns:
                missing_columns.append(col)

        if missing_columns:
            raise ValidationError(f"Colonnes manquantes: {', '.join(missing_columns)}")

    @classmethod
    def validate_data_types(cls, data):
        if not pd.api.types.is_numeric_dtype(data["Quantité d'article"]):
            raise ValidationError(
                "La colunne 'Quantité d'article' doit être numérique."
            )

        if not pd.api.types.is_numeric_dtype(data["Prix de l'article"]):
            raise ValidationError("La colonne 'Prix de l'article' doit être numérique.")

    @classmethod
    def validate_email_format(cls, email):
        email_domain = email.split("@")[-1]
        if "@" not in email or "." not in email_domain:
            raise ValidationError(f"Adresse e-mail invalide: {email}")

    @classmethod
    def validate_rows(cls, data):
        for index, row in data.iterrows():
            if row["Quantité d'article"] <= 0:
                raise ValidationError(f"Quantité invalide à la ligne {index + 1}")
            if row["Prix de l'article"] <= 0:
                raise ValidationError(f"Prix invalide à la ligne {index + 1}")
            cls.validate_email_format(row["Email du client"])
