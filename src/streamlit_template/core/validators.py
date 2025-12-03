"""
Validateurs de données pour l'application
"""

import re
from typing import Any

import streamlit as st


class ValidationError(Exception):
    """Exception pour les erreurs de validation"""
    pass


class Validator:
    """Classe de base pour les validateurs"""

    def __init__(self, error_message: str = "Validation échouée"):
        self.error_message = error_message

    def validate(self, value: Any) -> bool:
        """Méthode à surcharger pour la validation"""
        raise NotImplementedError

    def __call__(self, value: Any) -> Any:
        """Permet d'utiliser le validateur comme fonction"""
        if not self.validate(value):
            raise ValidationError(self.error_message)
        return value


class RequiredValidator(Validator):
    """Valide qu'une valeur n'est pas vide"""

    def __init__(self):
        super().__init__("Ce champ est requis")

    def validate(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, (list, dict)) and len(value) == 0:
            return False
        return True


class EmailValidator(Validator):
    """Valide un format d'email"""

    def __init__(self):
        super().__init__("Format d'email invalide")
        self.pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def validate(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return bool(self.pattern.match(value))


class LengthValidator(Validator):
    """Valide la longueur d'une chaîne"""

    def __init__(self, min_length: int = 0, max_length: int | None = None):
        self.min_length = min_length
        self.max_length = max_length
        message = f"Longueur doit être entre {min_length}"
        if max_length:
            message += f" et {max_length}"
        else:
            message += " et plus"
        super().__init__(message)

    def validate(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        length = len(value)
        if length < self.min_length:
            return False
        if self.max_length and length > self.max_length:
            return False
        return True


class NumericRangeValidator(Validator):
    """Valide qu'un nombre est dans une plage"""

    def __init__(self, min_val: float | None = None, max_val: float | None = None):
        self.min_val = min_val
        self.max_val = max_val
        message = "Valeur doit être"
        if min_val is not None:
            message += f" >= {min_val}"
        if max_val is not None:
            if min_val is not None:
                message += " et"
            message += f" <= {max_val}"
        super().__init__(message)

    def validate(self, value: Any) -> bool:
        if not isinstance(value, (int, float)):
            try:
                value = float(value)
            except (ValueError, TypeError):
                return False

        if self.min_val is not None and value < self.min_val:
            return False
        if self.max_val is not None and value > self.max_val:
            return False
        return True


class RegexValidator(Validator):
    """Valide avec une expression régulière"""

    def __init__(self, pattern: str, message: str = "Format invalide"):
        super().__init__(message)
        self.pattern = re.compile(pattern)

    def validate(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return bool(self.pattern.match(value))


class FileExtensionValidator(Validator):
    """Valide l'extension d'un fichier"""

    def __init__(self, allowed_extensions: list[str]):
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]
        super().__init__(f"Extensions autorisées: {', '.join(self.allowed_extensions)}")

    def validate(self, value: Any) -> bool:
        if not hasattr(value, 'name'):
            return False
        filename = value.name.lower()
        return any(filename.endswith(ext) for ext in self.allowed_extensions)


def validate_form_data(data: dict, validators: dict) -> dict:
    """
    Valide un dictionnaire de données avec des validateurs
    
    Args:
        data: Dictionnaire des données à valider
        validators: Dictionnaire {champ: [liste_validateurs]}
    
    Returns:
        Dict avec les erreurs par champ
    """
    errors = {}

    for field, field_validators in validators.items():
        if field not in data:
            continue

        value = data[field]

        for validator in field_validators:
            try:
                validator(value)
            except ValidationError as e:
                if field not in errors:
                    errors[field] = []
                errors[field].append(str(e))
                break  # Arrêter à la première erreur pour ce champ

    return errors


def display_validation_errors(errors: dict):
    """Affiche les erreurs de validation dans Streamlit"""
    if not errors:
        return

    with st.expander("❌ Erreurs de validation", expanded=True):
        for field, field_errors in errors.items():
            for error in field_errors:
                st.error(f"**{field}**: {error}")


# Validateurs pré-configurés courants
COMMON_VALIDATORS = {
    "required": RequiredValidator(),
    "email": EmailValidator(),
    "short_text": LengthValidator(1, 100),
    "long_text": LengthValidator(1, 1000),
    "positive_number": NumericRangeValidator(min_val=0),
    "percentage": NumericRangeValidator(0, 100),
    "phone": RegexValidator(r'^\+?[\d\s\-\(\)]+$', "Format de téléphone invalide"),
    "csv_file": FileExtensionValidator(['.csv']),
    "image_file": FileExtensionValidator(['.jpg', '.jpeg', '.png', '.gif'])
}
