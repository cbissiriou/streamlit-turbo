"""
Composants modaux et dialogs pour Streamlit
Note: Streamlit ne supporte pas nativement les modals, ces composants utilisent des alternatives
"""

import time
from collections.abc import Callable

import streamlit as st


class Modal:
    """
    Simulateur de modal utilisant les containers Streamlit
    """

    def __init__(self, title: str, key: str, max_width: int = 600):
        self.title = title
        self.key = key
        self.max_width = max_width
        self.is_open_key = f"modal_{key}_open"

    def is_open(self) -> bool:
        """Vérifie si le modal est ouvert"""
        return st.session_state.get(self.is_open_key, False)

    def open(self):
        """Ouvre le modal"""
        st.session_state[self.is_open_key] = True

    def close(self):
        """Ferme le modal"""
        st.session_state[self.is_open_key] = False

    def toggle(self):
        """Bascule l'état du modal"""
        st.session_state[self.is_open_key] = not self.is_open()

    def container(self):
        """
        Retourne un container pour le contenu du modal
        Utilise un expander pour simuler l'effet modal
        """
        if self.is_open():
            # Style CSS pour ressembler à un modal
            st.markdown(f"""
            <style>
            .modal-container {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                max-width: {self.max_width}px;
                width: 90%;
                z-index: 1000;
                padding: 0;
            }}
            
            .modal-overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 999;
            }}
            
            .modal-header {{
                background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
                color: white;
                padding: 1rem;
                border-radius: 12px 12px 0 0;
                font-weight: bold;
                font-size: 1.2rem;
            }}
            
            .modal-content {{
                padding: 1.5rem;
            }}
            </style>
            """, unsafe_allow_html=True)

            # Container principal du modal
            modal_container = st.container()

            with modal_container:
                # En-tête du modal
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### {self.title}")
                with col2:
                    if st.button("✕", key=f"{self.key}_close", help="Fermer"):
                        self.close()
                        st.rerun()

                st.markdown("---")

                return st.container()

        return None


def confirmation_dialog(
    message: str,
    title: str = "Confirmation",
    confirm_text: str = "Confirmer",
    cancel_text: str = "Annuler",
    key: str = "confirm_dialog"
) -> bool | None:
    """
    Affiche un dialog de confirmation
    
    Returns:
        True si confirmé, False si annulé, None si pas encore répondu
    """
    modal = Modal(title, key)

    # Ouvre automatiquement le modal s'il n'est pas déjà ouvert
    if not modal.is_open():
        modal.open()

    container = modal.container()

    if container:
        with container:
            st.markdown(f"**{message}**")
            st.markdown("")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button(f"✅ {confirm_text}", key=f"{key}_confirm", use_container_width=True):
                    modal.close()
                    return True

            with col2:
                if st.button(f"❌ {cancel_text}", key=f"{key}_cancel", use_container_width=True):
                    modal.close()
                    return False

    return None


def info_dialog(
    message: str,
    title: str = "Information",
    dialog_type: str = "info",
    key: str = "info_dialog"
) -> bool:
    """
    Affiche un dialog d'information
    
    Args:
        message: Message à afficher
        title: Titre du dialog
        dialog_type: Type (info, success, warning, error)
        key: Clé unique
    
    Returns:
        True si le dialog a été fermé
    """
    modal = Modal(title, key)

    if not modal.is_open():
        modal.open()

    container = modal.container()

    if container:
        with container:
            # Icône selon le type
            icons = {
                "info": "ℹ️",
                "success": "✅",
                "warning": "⚠️",
                "error": "❌"
            }

            icon = icons.get(dialog_type, "ℹ️")

            st.markdown(f"{icon} **{message}**")
            st.markdown("")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col2:
                if st.button("OK", key=f"{key}_ok", use_container_width=True):
                    modal.close()
                    st.rerun()
                    return True

    return False


def input_dialog(
    prompt: str,
    title: str = "Saisie",
    input_type: str = "text",
    default_value: str = "",
    key: str = "input_dialog"
) -> str | None:
    """
    Affiche un dialog de saisie
    
    Returns:
        La valeur saisie ou None si annulé
    """
    modal = Modal(title, key)

    if not modal.is_open():
        modal.open()

    container = modal.container()

    if container:
        with container:
            st.markdown(f"**{prompt}**")

            # Widget de saisie selon le type
            if input_type == "text":
                value = st.text_input("", value=default_value, key=f"{key}_input")
            elif input_type == "textarea":
                value = st.text_area("", value=default_value, key=f"{key}_input")
            elif input_type == "number":
                value = st.number_input("", value=float(default_value) if default_value else 0.0, key=f"{key}_input")
            elif input_type == "password":
                value = st.text_input("", type="password", key=f"{key}_input")
            else:
                value = st.text_input("", value=default_value, key=f"{key}_input")

            st.markdown("")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("✅ OK", key=f"{key}_ok", use_container_width=True):
                    modal.close()
                    return value

            with col3:
                if st.button("❌ Annuler", key=f"{key}_cancel", use_container_width=True):
                    modal.close()
                    return None

    return None


def progress_dialog(
    title: str = "Progression",
    message: str = "Traitement en cours...",
    key: str = "progress_dialog"
):
    """
    Affiche un dialog de progression
    """
    modal = Modal(title, key)

    if not modal.is_open():
        modal.open()

    container = modal.container()

    if container:
        with container:
            st.markdown(f"**{message}**")

            # Placeholder pour la barre de progression
            progress_bar = st.progress(0)
            status_text = st.empty()

            return progress_bar, status_text

    return None, None


def choice_dialog(
    message: str,
    choices: list,
    title: str = "Choix",
    key: str = "choice_dialog"
) -> str | None:
    """
    Affiche un dialog de choix multiple
    """
    modal = Modal(title, key)

    if not modal.is_open():
        modal.open()

    container = modal.container()

    if container:
        with container:
            st.markdown(f"**{message}**")

            selected = st.radio("", choices, key=f"{key}_radio")

            st.markdown("")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("✅ Choisir", key=f"{key}_choose", use_container_width=True):
                    modal.close()
                    return selected

            with col3:
                if st.button("❌ Annuler", key=f"{key}_cancel", use_container_width=True):
                    modal.close()
                    return None

    return None


def file_dialog(
    title: str = "Sélection de fichier",
    accept_multiple: bool = False,
    file_types: list = None,
    key: str = "file_dialog"
):
    """
    Dialog de sélection de fichier
    """
    modal = Modal(title, key, max_width=800)

    if not modal.is_open():
        modal.open()

    container = modal.container()

    if container:
        with container:
            uploaded_files = st.file_uploader(
                "Choisissez un fichier",
                accept_multiple_files=accept_multiple,
                type=file_types,
                key=f"{key}_uploader"
            )

            st.markdown("")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("✅ OK", key=f"{key}_ok", use_container_width=True):
                    modal.close()
                    return uploaded_files

            with col3:
                if st.button("❌ Annuler", key=f"{key}_cancel", use_container_width=True):
                    modal.close()
                    return None

    return None


def custom_dialog(content_func: Callable, title: str, key: str, **kwargs):
    """
    Dialog personnalisé avec fonction de contenu
    
    Args:
        content_func: Fonction qui génère le contenu du dialog
        title: Titre du dialog
        key: Clé unique
        **kwargs: Arguments passés à content_func
    """
    modal = Modal(title, key)

    if not modal.is_open():
        modal.open()

    container = modal.container()

    if container:
        with container:
            result = content_func(**kwargs)

            # Boutons par défaut si la fonction ne les gère pas
            if not st.session_state.get(f"{key}_handled", False):
                st.markdown("")

                col1, col2, col3 = st.columns([1, 1, 1])

                with col2:
                    if st.button("Fermer", key=f"{key}_close", use_container_width=True):
                        modal.close()
                        st.rerun()

            return result

    return None


class DialogManager:
    """Gestionnaire de dialogs pour éviter les conflits"""

    def __init__(self):
        self.active_dialogs = set()

    def show_confirmation(
        self,
        message: str,
        title: str = "Confirmation",
        key: str = "confirmation"
    ) -> bool | None:
        """Affiche un dialog de confirmation en gérant les conflits"""
        if key not in self.active_dialogs:
            self.active_dialogs.add(key)

        result = confirmation_dialog(message, title, key=key)

        if result is not None:
            self.active_dialogs.discard(key)

        return result

    def show_info(
        self,
        message: str,
        title: str = "Information",
        dialog_type: str = "info",
        key: str = "info"
    ) -> bool:
        """Affiche un dialog d'information"""
        if key not in self.active_dialogs:
            self.active_dialogs.add(key)

        result = info_dialog(message, title, dialog_type, key)

        if result:
            self.active_dialogs.discard(key)

        return result

    def show_input(
        self,
        prompt: str,
        title: str = "Saisie",
        input_type: str = "text",
        default_value: str = "",
        key: str = "input"
    ) -> str | None:
        """Affiche un dialog de saisie"""
        if key not in self.active_dialogs:
            self.active_dialogs.add(key)

        result = input_dialog(prompt, title, input_type, default_value, key)

        if result is not None:
            self.active_dialogs.discard(key)

        return result


# Instance globale du gestionnaire
dialog_manager = DialogManager()


def toast_notification(
    message: str,
    notification_type: str = "info",
    duration: float = 3.0
):
    """
    Affiche une notification toast (temporaire)
    
    Args:
        message: Message à afficher
        notification_type: Type (info, success, warning, error)
        duration: Durée d'affichage en secondes
    """
    # Utilise st.toast si disponible (Streamlit >= 1.27)
    if hasattr(st, 'toast'):
        if notification_type == "success":
            st.toast(f"✅ {message}", icon="✅")
        elif notification_type == "warning":
            st.toast(f"⚠️ {message}", icon="⚠️")
        elif notification_type == "error":
            st.toast(f"❌ {message}", icon="❌")
        else:
            st.toast(f"ℹ️ {message}", icon="ℹ️")
    else:
        # Fallback pour versions antérieures
        placeholder = st.empty()

        if notification_type == "success":
            placeholder.success(message)
        elif notification_type == "warning":
            placeholder.warning(message)
        elif notification_type == "error":
            placeholder.error(message)
        else:
            placeholder.info(message)

        # Supprime après la durée spécifiée
        time.sleep(duration)
        placeholder.empty()


def sidebar_modal(title: str, content_func: Callable, key: str = "sidebar_modal"):
    """
    Modal dans la sidebar
    """
    with st.sidebar:
        if st.button(f"📋 {title}", key=f"{key}_trigger"):
            st.session_state[f"{key}_open"] = True

        if st.session_state.get(f"{key}_open", False):
            st.markdown("---")
            st.markdown(f"### {title}")

            result = content_func()

            if st.button("❌ Fermer", key=f"{key}_close"):
                st.session_state[f"{key}_open"] = False
                st.rerun()

            return result

    return None
