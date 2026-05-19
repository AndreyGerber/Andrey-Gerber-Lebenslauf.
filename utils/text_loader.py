from data.texts import de, en, ru

LANG_MAP = {
    "de": de.TEXTS,
    "en": en.TEXTS,
    "ru": ru.TEXTS
}

def get_text(key, lang="de"):
    return LANG_MAP.get(lang, {}).get(key, key)