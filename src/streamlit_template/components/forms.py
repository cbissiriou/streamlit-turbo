"""
Composants de formulaires avancés et réutilisables
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional, Callable, Union
from datetime import datetime, date, time
import re

from ..core import validate_form_data, COMMON_VALIDATORS, ValidationError
from ..utils import create_info_box


def create_form_field(
    field_type: str,
    key: str,
    label: str,
    value: Any = None,
    help_text: Optional[str] = None,
    required: bool = False,
    validators: List = None,
    **kwargs
) -> Any:
    """
    Crée un champ de formulaire générique avec validation
    
    Args:
        field_type: Type de champ (text, email, number, etc.)
        key: Clé unique pour le champ
        label: Label affiché
        value: Valeur par défaut
        help_text: Texte d'aide
        required: Champ obligatoire
        validators: Liste des validateurs
        **kwargs: Arguments supplémentaires pour le widget
    """
    # Ajoute l'indicateur de champ requis
    display_label = f"{label} *" if required else label
    
    # Widgets selon le type
    if field_type == "text":
        result = st.text_input(display_label, value or "", key=key, help=help_text, **kwargs)
    
    elif field_type == "email":
        result = st.text_input(
            display_label, 
            value or "", 
            key=key, 
            help=help_text or "Format: exemple@domain.com",
            **kwargs
        )
    
    elif field_type == "password":
        result = st.text_input(
            display_label, 
            value or "", 
            type="password", 
            key=key, 
            help=help_text,
            **kwargs
        )
    
    elif field_type == "textarea":
        result = st.text_area(display_label, value or "", key=key, help=help_text, **kwargs)
    
    elif field_type == "number":
        result = st.number_input(display_label, value=value, key=key, help=help_text, **kwargs)
    
    elif field_type == "slider":
        min_val = kwargs.pop('min_value', 0)
        max_val = kwargs.pop('max_value', 100)
        result = st.slider(display_label, min_val, max_val, value or min_val, key=key, help=help_text, **kwargs)
    
    elif field_type == "selectbox":
        options = kwargs.pop('options', [])
        result = st.selectbox(display_label, options, index=0 if value is None else options.index(value) if value in options else 0, key=key, help=help_text, **kwargs)
    
    elif field_type == "multiselect":
        options = kwargs.pop('options', [])
        result = st.multiselect(display_label, options, default=value or [], key=key, help=help_text, **kwargs)
    
    elif field_type == "radio":
        options = kwargs.pop('options', [])
        result = st.radio(display_label, options, index=0 if value is None else options.index(value) if value in options else 0, key=key, help=help_text, **kwargs)
    
    elif field_type == "checkbox":
        result = st.checkbox(display_label, value=value or False, key=key, help=help_text, **kwargs)
    
    elif field_type == "date":
        result = st.date_input(display_label, value=value, key=key, help=help_text, **kwargs)
    
    elif field_type == "time":
        result = st.time_input(display_label, value=value, key=key, help=help_text, **kwargs)
    
    elif field_type == "datetime":
        col1, col2 = st.columns(2)
        with col1:
            date_val = st.date_input(f"{display_label} (Date)", value=value.date() if value else None, key=f"{key}_date", help=help_text)
        with col2:
            time_val = st.time_input(f"{display_label} (Heure)", value=value.time() if value else None, key=f"{key}_time")
        
        if date_val and time_val:
            result = datetime.combine(date_val, time_val)
        else:
            result = None
    
    elif field_type == "file":
        result = st.file_uploader(display_label, key=key, help=help_text, **kwargs)
    
    elif field_type == "color":
        result = st.color_picker(display_label, value=value or "#000000", key=key, help=help_text, **kwargs)
    
    else:
        st.error(f"Type de champ non supporté: {field_type}")
        result = None
    
    return result


class FormBuilder:
    """Constructeur de formulaires avancé"""
    
    def __init__(self, form_key: str, title: Optional[str] = None):
        self.form_key = form_key
        self.title = title
        self.fields = {}
        self.validators = {}
        self.form_data = {}
        self.errors = {}
        
    def add_field(
        self,
        field_name: str,
        field_type: str,
        label: str,
        required: bool = False,
        validators: List = None,
        **field_kwargs
    ):
        """Ajoute un champ au formulaire"""
        self.fields[field_name] = {
            'type': field_type,
            'label': label,
            'required': required,
            'kwargs': field_kwargs
        }
        
        # Ajoute les validateurs
        field_validators = []
        if required:
            field_validators.append(COMMON_VALIDATORS['required'])
        if validators:
            field_validators.extend(validators)
        
        if field_validators:
            self.validators[field_name] = field_validators
        
        return self
    
    def add_section(self, title: str, description: Optional[str] = None):
        """Ajoute une section au formulaire"""
        st.markdown(f"### {title}")
        if description:
            st.markdown(f"*{description}*")
        st.markdown("---")
        return self
    
    def render(self) -> Dict[str, Any]:
        """Rend le formulaire et retourne les données"""
        if self.title:
            st.markdown(f"## {self.title}")
        
        with st.form(key=self.form_key):
            form_data = {}
            
            # Rend chaque champ
            for field_name, field_config in self.fields.items():
                value = create_form_field(
                    field_config['type'],
                    f"{self.form_key}_{field_name}",
                    field_config['label'],
                    required=field_config['required'],
                    **field_config['kwargs']
                )
                form_data[field_name] = value
            
            # Bouton de soumission
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                submitted = st.form_submit_button("✅ Valider", use_container_width=True)
            
            with col2:
                if st.form_submit_button("🔄 Réinitialiser", use_container_width=True):
                    st.rerun()
            
            # Validation si soumis
            if submitted:
                self.errors = validate_form_data(form_data, self.validators)
                
                if not self.errors:
                    self.form_data = form_data
                    st.success("✅ Formulaire validé avec succès!")
                    return form_data
                else:
                    st.error("❌ Veuillez corriger les erreurs ci-dessous:")
                    for field, field_errors in self.errors.items():
                        for error in field_errors:
                            st.error(f"**{field}**: {error}")
        
        return {}


def create_contact_form() -> Dict[str, Any]:
    """Formulaire de contact pré-configuré"""
    form = FormBuilder("contact_form", "📧 Formulaire de contact")
    
    form.add_section("Informations personnelles")
    form.add_field("nom", "text", "Nom complet", required=True, validators=[COMMON_VALIDATORS['short_text']])
    form.add_field("email", "email", "Adresse email", required=True, validators=[COMMON_VALIDATORS['email']])
    form.add_field("telephone", "text", "Téléphone", validators=[COMMON_VALIDATORS['phone']])
    
    form.add_section("Message")
    form.add_field("sujet", "selectbox", "Sujet", required=True, 
                   options=["Information générale", "Support technique", "Demande commerciale", "Autre"])
    form.add_field("message", "textarea", "Votre message", required=True, 
                   validators=[COMMON_VALIDATORS['long_text']], height=150)
    
    form.add_section("Préférences")
    form.add_field("newsletter", "checkbox", "S'abonner à la newsletter")
    form.add_field("contact_pref", "radio", "Moyen de contact préféré", 
                   options=["Email", "Téléphone", "Pas de préférence"])
    
    return form.render()


def create_user_profile_form() -> Dict[str, Any]:
    """Formulaire de profil utilisateur"""
    form = FormBuilder("user_profile", "👤 Profil utilisateur")
    
    form.add_section("Informations de base")
    form.add_field("prenom", "text", "Prénom", required=True)
    form.add_field("nom", "text", "Nom", required=True)
    form.add_field("email", "email", "Email", required=True, validators=[COMMON_VALIDATORS['email']])
    form.add_field("date_naissance", "date", "Date de naissance")
    
    form.add_section("Informations professionnelles")
    form.add_field("entreprise", "text", "Entreprise")
    form.add_field("poste", "text", "Poste/Fonction")
    form.add_field("secteur", "selectbox", "Secteur d'activité",
                   options=["Technologies", "Finance", "Santé", "Éducation", "Commerce", "Autre"])
    form.add_field("experience", "slider", "Années d'expérience", 
                   min_value=0, max_value=40, value=5)
    
    form.add_section("Préférences")
    form.add_field("competences", "multiselect", "Compétences",
                   options=["Python", "JavaScript", "Data Science", "Machine Learning", "Web Dev", "Mobile"])
    form.add_field("photo", "file", "Photo de profil", 
                   accept_multiple_files=False, type=['jpg', 'jpeg', 'png'])
    
    return form.render()


def create_survey_form(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Crée un formulaire de sondage dynamique
    
    Args:
        questions: Liste des questions avec format:
        [
            {
                'id': 'q1',
                'text': 'Question text',
                'type': 'selectbox|radio|slider|text|textarea',
                'options': [...],  # pour selectbox/radio
                'required': True/False
            }
        ]
    """
    form = FormBuilder("survey_form", "📋 Questionnaire")
    
    form.add_section("Questionnaire", "Veuillez répondre aux questions suivantes:")
    
    for question in questions:
        q_id = question['id']
        q_text = question['text']
        q_type = question['type']
        q_required = question.get('required', False)
        q_options = question.get('options', [])
        
        if q_type in ['selectbox', 'radio', 'multiselect']:
            form.add_field(q_id, q_type, q_text, required=q_required, options=q_options)
        elif q_type == 'slider':
            min_val = question.get('min', 1)
            max_val = question.get('max', 5)
            form.add_field(q_id, q_type, q_text, required=q_required, 
                          min_value=min_val, max_value=max_val)
        else:
            form.add_field(q_id, q_type, q_text, required=q_required)
    
    return form.render()


def create_data_upload_form() -> Dict[str, Any]:
    """Formulaire d'upload de données avec validation"""
    form = FormBuilder("data_upload", "📁 Import de données")
    
    form.add_section("Fichier de données")
    form.add_field("file", "file", "Sélectionner un fichier", required=True,
                   type=['csv', 'xlsx', 'json'], validators=[COMMON_VALIDATORS['csv_file']])
    
    form.add_section("Configuration d'import")
    form.add_field("separator", "selectbox", "Séparateur CSV", 
                   options=[",", ";", "\t", "|"], help="Séparateur pour les fichiers CSV")
    form.add_field("encoding", "selectbox", "Encodage",
                   options=["utf-8", "latin-1", "cp1252"])
    form.add_field("header", "checkbox", "Première ligne = en-têtes", value=True)
    
    form.add_section("Validation")
    form.add_field("validate_data", "checkbox", "Valider les données", value=True,
                   help="Vérifie la cohérence des données importées")
    form.add_field("remove_duplicates", "checkbox", "Supprimer les doublons", value=True)
    
    return form.render()


def create_settings_form() -> Dict[str, Any]:
    """Formulaire de paramètres de l'application"""
    form = FormBuilder("app_settings", "⚙️ Paramètres de l'application")
    
    form.add_section("Interface utilisateur")
    form.add_field("theme", "selectbox", "Thème",
                   options=["Light", "Dark", "Auto"])
    form.add_field("language", "selectbox", "Langue",
                   options=["Français", "English", "Español"])
    form.add_field("sidebar_default", "selectbox", "État sidebar par défaut",
                   options=["Expanded", "Collapsed"])
    
    form.add_section("Notifications")
    form.add_field("email_notifications", "checkbox", "Notifications par email", value=True)
    form.add_field("browser_notifications", "checkbox", "Notifications navigateur")
    form.add_field("notification_frequency", "radio", "Fréquence des notifications",
                   options=["Immédiate", "Quotidienne", "Hebdomadaire"])
    
    form.add_section("Performance")
    form.add_field("cache_duration", "slider", "Durée cache (heures)",
                   min_value=1, max_value=24, value=6)
    form.add_field("auto_refresh", "checkbox", "Actualisation automatique")
    form.add_field("refresh_interval", "number", "Intervalle d'actualisation (sec)",
                   min_value=30, max_value=300, value=60)
    
    return form.render()


def create_search_form() -> Dict[str, Any]:
    """Formulaire de recherche avancée"""
    with st.form("search_form"):
        st.markdown("### 🔍 Recherche avancée")
        
        col1, col2 = st.columns(2)
        
        with col1:
            query = st.text_input("🔎 Recherche", placeholder="Entrez vos mots-clés...")
            category = st.selectbox("📂 Catégorie", 
                                   options=["Toutes", "Documents", "Images", "Vidéos", "Autres"])
        
        with col2:
            date_range = st.date_input("📅 Période", value=[], help="Sélectionnez une plage de dates")
            sort_by = st.selectbox("📊 Trier par",
                                  options=["Pertinence", "Date (récent)", "Date (ancien)", "Nom", "Taille"])
        
        # Filtres avancés
        with st.expander("🔧 Filtres avancés"):
            col1, col2 = st.columns(2)
            
            with col1:
                min_size = st.number_input("Taille min (MB)", min_value=0, value=0)
                include_tags = st.text_input("Tags à inclure", placeholder="tag1, tag2, ...")
            
            with col2:
                max_size = st.number_input("Taille max (MB)", min_value=0, value=0)
                exclude_tags = st.text_input("Tags à exclure", placeholder="tag1, tag2, ...")
        
        # Options d'affichage
        with st.expander("👁️ Options d'affichage"):
            results_per_page = st.slider("Résultats par page", 10, 100, 25)
            show_preview = st.checkbox("Aperçu des résultats", value=True)
        
        submitted = st.form_submit_button("🔍 Rechercher", use_container_width=True)
        
        if submitted:
            return {
                'query': query,
                'category': category,
                'date_range': list(date_range) if date_range else [],
                'sort_by': sort_by,
                'min_size': min_size,
                'max_size': max_size if max_size > 0 else None,
                'include_tags': [tag.strip() for tag in include_tags.split(',') if tag.strip()],
                'exclude_tags': [tag.strip() for tag in exclude_tags.split(',') if tag.strip()],
                'results_per_page': results_per_page,
                'show_preview': show_preview
            }
    
    return {}


def display_form_summary(form_data: Dict[str, Any], title: str = "📋 Résumé du formulaire"):
    """Affiche un résumé des données de formulaire"""
    if not form_data:
        return
    
    create_info_box(
        title="📋 Données soumises",
        content="Vos informations ont été enregistrées avec succès.",
        type="success"
    )
    
    with st.expander("Voir le détail des données"):
        for key, value in form_data.items():
            if isinstance(value, (str, int, float, bool)):
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            elif isinstance(value, list):
                st.write(f"**{key.replace('_', ' ').title()}:** {', '.join(map(str, value))}")
            elif hasattr(value, 'name'):  # Fichier uploadé
                st.write(f"**{key.replace('_', ' ').title()}:** {value.name}")
            else:
                st.write(f"**{key.replace('_', ' ').title()}:** {type(value).__name__}")


def create_wizard_form(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Crée un formulaire en étapes (wizard)
    
    Args:
        steps: Liste des étapes avec leurs champs
    """
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 0
        st.session_state.wizard_data = {}
    
    current_step = st.session_state.wizard_step
    total_steps = len(steps)
    
    # Barre de progression
    progress = (current_step + 1) / total_steps
    st.progress(progress)
    st.caption(f"Étape {current_step + 1} sur {total_steps}")
    
    # Affiche l'étape actuelle
    step_config = steps[current_step]
    st.markdown(f"## {step_config['title']}")
    
    if 'description' in step_config:
        st.markdown(step_config['description'])
    
    with st.form(f"wizard_step_{current_step}"):
        step_data = {}
        
        for field in step_config['fields']:
            value = create_form_field(
                field['type'],
                field['key'],
                field['label'],
                **field.get('kwargs', {})
            )
            step_data[field['key']] = value
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if current_step > 0:
                prev_clicked = st.form_submit_button("⬅️ Précédent")
            else:
                prev_clicked = False
        
        with col2:
            if current_step < total_steps - 1:
                next_clicked = st.form_submit_button("Suivant ➡️")
                finish_clicked = False
            else:
                next_clicked = False
                finish_clicked = st.form_submit_button("✅ Terminer")
        
        with col3:
            cancel_clicked = st.form_submit_button("❌ Annuler")
        
        # Navigation
        if prev_clicked and current_step > 0:
            st.session_state.wizard_step = current_step - 1
            st.rerun()
        
        elif next_clicked and current_step < total_steps - 1:
            st.session_state.wizard_data.update(step_data)
            st.session_state.wizard_step = current_step + 1
            st.rerun()
        
        elif finish_clicked:
            st.session_state.wizard_data.update(step_data)
            final_data = st.session_state.wizard_data.copy()
            
            # Reset wizard
            st.session_state.wizard_step = 0
            st.session_state.wizard_data = {}
            
            return final_data
        
        elif cancel_clicked:
            st.session_state.wizard_step = 0
            st.session_state.wizard_data = {}
            st.rerun()
    
    return {}