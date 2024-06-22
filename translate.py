from googletrans import Translator

def check_language(text):
    translator = Translator()
    translation = translator.translate(text)
    return translation.src

def from_ka_to_en(text):
    translator = Translator()
    translation = translator.translate(text,src='ka', dest='en')
    return translation.text

def from_en_to_ka(text):
    translator = Translator()
    translation = translator.translate(text,src='en', dest='ka')
    return translation.text

