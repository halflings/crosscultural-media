import time

import goslate
import newspaper

import config
from news import GoogleNews

def fetch_translations(query, original_language):
    if original_language not in config.SUPPORTED_LANGUAGES:
        print "'{}' is not supported".format(original_language)
        return

    translations = []
    translations.append((original_language, query))

    gs = goslate.Goslate()
    for language in config.SUPPORTED_LANGUAGES:
        if language == original_language:
            continue
        translated_query = gs.translate(query, language)
        translations.append((language, translated_query))
    return translations

def process_query(query, original_language):
    translations = fetch_translations(query, original_language)

    for language, translated_query in translations:
        print u"* Query '{}' in '{}'".format(translated_query, language)
        fetch_articles(translated_query, language)

def fetch_articles(query, language):
    api = GoogleNews()
    entries = api.news(query, language)
    articles = []
    for entry in entries:
        print u"    . Article '{}'".format(entry.title)
        article = newspaper.Article(entry.link, language=language)

        article.download()
        article.parse()
        article.nlp()

        articles.append(article)
    return articles

if __name__ == '__main__':
    print process_query("mariage", "fr")