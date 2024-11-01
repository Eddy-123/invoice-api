import decimal
import pandas as pd
from django.core.exceptions import ValidationError
from invoices.helpers import is_convertible_to_number


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

        if data["Nom du client"].isnull().any():
            empty_indexes = cls.get_empty_indexes_of_column(data, "Nom du client")
            raise ValidationError(
                f"La colonne 'Nom du client' n'est pas completement remplie. Lignes: {[x + 2 for x in empty_indexes]}"
            )

        if data["Prix de l'article"].isnull().any():
            empty_indexes = cls.get_empty_indexes_of_column(data, "Prix de l'article")

            raise ValidationError(
                f"La colonne 'Prix de l'article' n'est pas completement remplie. Lignes: {[x + 2 for x in empty_indexes]}"
            )

        if data["Quantité d'article"].isnull().any():
            empty_indexes = cls.get_empty_indexes_of_column(data, "Quantité d'article")

            raise ValidationError(
                f"La colonne 'Quantité d'article' n'est pas completement remplie. Lignes: {[x + 2 for x in empty_indexes]}"
            )

        if data["Description de l'article"].isnull().any():
            empty_indexes = cls.get_empty_indexes_of_column(
                data, "Description de l'article"
            )

            raise ValidationError(
                f"La colonne 'Description de l'article' n'est pas completement remplie. Lignes: {[x + 2 for x in empty_indexes]}"
            )

        if data["Email du client"].isnull().any():
            empty_indexes = cls.get_empty_indexes_of_column(data, "Email du client")

            raise ValidationError(
                f"La colonne 'Email du client' n'est pas completement remplie. Lignes: {[x + 2 for x in empty_indexes]}"
            )

    @classmethod
    def validate_data_types(cls, data):
        if not pd.api.types.is_numeric_dtype(data["Quantité d'article"]):
            raise ValidationError(
                "La colunne 'Quantité d'article' doit être numérique."
            )

        if not pd.api.types.is_numeric_dtype(data["Prix de l'article"]):
            non_numeric_rows = data[
                data["Prix de l'article"].apply(
                    lambda x: not is_convertible_to_number(x)
                )
            ]

            raise ValidationError(
                f"La colonne 'Prix de l'article' doit être numérique."
                f"Les lignes suivantes contiennent des valeurs invalides :\n{non_numeric_rows.to_string(header=False, index=False)}"
            )

        if not pd.api.types.is_string_dtype(data["Nom du client"]):
            non_string_rows = data[
                data["Nom du client"].apply(lambda x: not isinstance(x, str))
            ]

            if not non_string_rows.empty:
                raise ValidationError(
                    f"La colonne 'Nom du client' doit être un texte. "
                    f"Les lignes suivantes contiennent des valeurs non textuelles :\n{non_string_rows.to_string(header=False, index=False)}"
                )

    @classmethod
    def validate_email_format(cls, email):
        email_domain = email.split("@")[-1]
        if "@" not in email or "." not in email_domain:
            raise ValidationError(f"Adresse e-mail invalide: {email}")

    @classmethod
    def validate_rows(cls, data):
        for index, row in data.iterrows():
            if row["Quantité d'article"] < 0:
                raise ValidationError(f"Quantité invalide à la ligne {index + 1}")
            if row["Prix de l'article"] <= 0:
                raise ValidationError(f"Prix invalide à la ligne {index + 1}")
            cls.validate_email_format(row["Email du client"])

    @classmethod
    def get_empty_indexes_of_column(cls, data, column):
        return data[data[column].isnull() | (data[column] == "")].index.tolist()
