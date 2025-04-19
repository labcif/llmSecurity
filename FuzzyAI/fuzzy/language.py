_selected_language = 'en'

def set_language(lang: str):
    global _selected_language
    _selected_language = lang

def get_language() -> str:
    return _selected_language