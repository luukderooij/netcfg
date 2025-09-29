import json
import os
import logging

logger = logging.getLogger(__name__)  # module-specifieke logger

CONFIG_FILE = "config.json"

# Standaard instellingen
DEFAULT_SETTINGS = {
    "last_adapter": None,
    "window_size": "700x500",
    "theme": "light"
}

_settings = DEFAULT_SETTINGS.copy()

def load_settings():
    """Laad instellingen uit config.json, indien aanwezig."""
    global _settings
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                _settings.update(data)
                logger.debug("Instellingen geladen uit %s", CONFIG_FILE)
        except Exception as e:
            logger.warning("Kon instellingen niet laden: %s", e)

def save_settings():
    """Sla huidige instellingen op naar config.json."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(_settings, f, indent=2)
            logger.debug("Instellingen opgeslagen naar %s", CONFIG_FILE)
    except Exception as e:
        logger.error("Kon instellingen niet opslaan: %s", e)

def get(key, default=None):
    """Lees een instelling uit, met optionele default."""
    return _settings.get(key, default)

def set(key, value):
    """Stel een instelling in (in geheugen, niet direct persistent)."""
    _settings[key] = value
    logger.debug("Instelling gewijzigd: %s = %s", key, value)
