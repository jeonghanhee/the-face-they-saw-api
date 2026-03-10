from pathlib import Path
from babel.support import Translations

LOCALES_DIR = Path(__file__).parent.parent / "locales"

translations_cache = {
    "ko": Translations.load(LOCALES_DIR, locales=["ko_KR"]),
    "en": Translations.load(LOCALES_DIR, locales=["en_US"]),
}

def get_translation(lang: str):
    return translations_cache.get(lang.lower(), translations_cache["ko"]).gettext