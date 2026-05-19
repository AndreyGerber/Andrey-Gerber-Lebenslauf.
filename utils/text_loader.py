from data.texts import de, en, ru

TEXTS = {
    "de": de.TEXTS,
    "en": en.TEXTS,
    "ru": ru.TEXTS
}

def get_text(lang="de"):
    return TEXTS.get(lang, TEXTS["de"])