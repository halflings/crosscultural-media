import time

import extractor
import goslate
import mongoengine
import newspaper

import config
from gavagai import Gavagai
from model import Article, Query, QueryJob
from news import GoogleNews


def fetch_translations(query_job):
    if query_job.language not in config.SUPPORTED_LANGUAGES:
        print "'{}' is not supported".format(query_job.language)
        return

    original_query = Query(text=query_job.text, language=query_job.language, source=query_job).save()

    translations = []
    translations.append(original_query)

    gs = goslate.Goslate()
    for language in config.SUPPORTED_LANGUAGES:
        if language == query_job.language:
            continue
        translated_text = gs.translate(query_job.text, language)
        translated_query = Query(
            text=translated_text, language=language, source=query_job).save()
        translations.append(translated_query)
    return translations


def fetch_articles(query):
    api = GoogleNews()
    entries = api.news(query.text, query.language)
    articles = []
    for entry in entries:
        print u"    . Article '{}'".format(entry.title)
        nws_article = newspaper.Article(entry.link, language=query.language)

        nws_article.download()
        nws_article.parse()
        nws_article.nlp()

        summary = nws_article.summary # '. '.join(extractor.extract_surrounded_context(nws_article.text, query.text))
        article = Article(
            title=nws_article.title, text=summary, query=query).save()
        articles.append(article)
    return articles

def fetch_scores(article):
    gavagai = Gavagai(config.GAVAGAI_API_KEY)
    resp = gavagai.tonality([article.text], article.query.language)
    article.build_scores(resp)

def queue_query(query, original_language):
    QueryJob(text=query, language=original_language).save()

def process_query(query_job):
    queries = fetch_translations(query_job)

    for query in queries:
        articles = fetch_articles(query)
        for article in articles:
            fetch_scores(article)

    query_job.processed = True
    query_job.save()

def processing_routine():
    unprocessed_queries = QueryJob.objects(processed=False)
    for query_job in unprocessed_queries:
        print "! Processing the query job : {}".format(query_job)
        process_query(query_job)

if __name__ == '__main__':
    import sys
    db = mongoengine.connect('testdb')
    # db.drop_database('testdb')

    query = "death"
    if len(sys.argv) > 1:
        query = sys.argv[1]

    queue_query(query, "en")
    processing_routine()

    # while True:
    #     processing_routine()
    #     time.sleep(0.5)