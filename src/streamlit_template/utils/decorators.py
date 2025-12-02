"""
Décorateurs utilitaires pour l'application
"""

import time
import streamlit as st
from functools import wraps
from typing import Any, Callable, Optional
import logging


def measure_time(func: Callable = None, *, display: bool = False) -> Callable:
    """
    Décorateur pour mesurer le temps d'exécution d'une fonction
    
    Args:
        display: Si True, affiche le temps dans Streamlit
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = f(*args, **kwargs)
            execution_time = time.time() - start_time
            
            if display:
                st.caption(f"⏱️ Temps d'exécution: {execution_time:.2f}s")
            
            # Stocke le temps dans les métriques de session si disponible
            if hasattr(st.session_state, 'execution_times'):
                st.session_state.execution_times[f.__name__] = execution_time
            
            return result
        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)


def with_spinner(message: str = "Chargement..."):
    """Décorateur pour afficher un spinner pendant l'exécution"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def handle_errors(default_return: Any = None, show_error: bool = True):
    """
    Décorateur pour gérer les erreurs de façon élégante
    
    Args:
        default_return: Valeur à retourner en cas d'erreur
        show_error: Si True, affiche l'erreur dans Streamlit
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if show_error:
                    st.error(f"Erreur dans {func.__name__}: {str(e)}")
                
                # Log l'erreur
                logging.error(f"Erreur dans {func.__name__}: {str(e)}", exc_info=True)
                
                # Stocke l'erreur dans l'état de session
                if 'last_errors' not in st.session_state:
                    st.session_state.last_errors = []
                st.session_state.last_errors.append({
                    'function': func.__name__,
                    'error': str(e),
                    'timestamp': time.time()
                })
                
                return default_return
        return wrapper
    return decorator


def require_authentication(redirect_to: str = "login"):
    """Décorateur pour s'assurer qu'un utilisateur est authentifié"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Vérifie l'authentification (à adapter selon votre système)
            if not st.session_state.get('authenticated', False):
                st.warning("Vous devez être connecté pour accéder à cette page.")
                st.info(f"Redirecting to {redirect_to}...")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_result(ttl: int = 3600, key_prefix: str = ""):
    """
    Décorateur pour mettre en cache le résultat d'une fonction
    
    Args:
        ttl: Temps de vie du cache en secondes
        key_prefix: Préfixe pour la clé de cache
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Génère une clé unique basée sur les arguments
            cache_key = f"{key_prefix}_{func.__name__}_{hash(str(args) + str(kwargs))}"
            
            # Vérifie si le résultat est en cache
            if cache_key in st.session_state:
                cached_data = st.session_state[cache_key]
                if time.time() - cached_data['timestamp'] < ttl:
                    return cached_data['result']
            
            # Exécute la fonction et met en cache
            result = func(*args, **kwargs)
            st.session_state[cache_key] = {
                'result': result,
                'timestamp': time.time()
            }
            
            return result
        return wrapper
    return decorator


def log_function_call(level: str = "INFO"):
    """Décorateur pour logger les appels de fonction"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            
            # Log avant l'exécution
            logger.log(getattr(logging, level.upper()), 
                      f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log après l'exécution
            logger.log(getattr(logging, level.upper()),
                      f"Completed {func.__name__} in {execution_time:.2f}s")
            
            return result
        return wrapper
    return decorator


def validate_inputs(**validators):
    """
    Décorateur pour valider les arguments d'entrée
    
    Args:
        **validators: Dict des validateurs par nom d'argument
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtient les noms des paramètres de la fonction
            import inspect
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())
            
            # Combine args et kwargs
            all_args = dict(zip(param_names, args))
            all_args.update(kwargs)
            
            # Valide chaque argument
            for param_name, validator in validators.items():
                if param_name in all_args:
                    value = all_args[param_name]
                    if not validator(value):
                        raise ValueError(f"Validation failed for parameter '{param_name}' with value {value}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def streamlit_fragment(func: Callable = None):
    """
    Décorateur pour marquer une fonction comme fragment Streamlit
    (pour une exécution partielle)
    """
    def decorator(f: Callable) -> Callable:
        @st.fragment
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Décorateur pour retry automatique en cas d'échec
    
    Args:
        max_attempts: Nombre maximum de tentatives
        delay: Délai entre les tentatives en secondes
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:  # Pas le dernier essai
                        time.sleep(delay)
                        continue
                    else:
                        raise last_exception
            
            return None  # Ne devrait jamais arriver
        return wrapper
    return decorator