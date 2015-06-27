from modeltranslation.translator import translator, TranslationOptions
from core.models import HomePage, ContactFormPage


class HomePageTranslationOptions(TranslationOptions):
    fields = ('body',)


class ContactFormPageTranslationOptions(TranslationOptions):
    fields = ('intro', 'thank_you_text',)


translator.register(HomePage, HomePageTranslationOptions)
translator.register(ContactFormPage, ContactFormPageTranslationOptions)