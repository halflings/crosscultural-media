import config
import gavagai
import newspaper

def gavagai_test():
    print "# GAVAGAI (gavagai module):"
    print

    api = gavagai.Gavagai(config.GAVAGAI_API_KEY)
    texts = ["I am angry, I hate you, blah blah, you're terrible.",
             "I am happy. Cats are cute, flowers smell good.",
             "Stockholm is Sweden's capital. It isn't close to Beijing."]
    response = api.tonality(texts, "en")

    for text_id, text in enumerate(texts):
        print text
        for resp in response['texts']:
            if resp['id'] == str(text_id):
                break
        for tone in sorted(resp['tonality'], key=lambda t : t['score'], reverse=True):
            print "* {} = {}".format(tone['tone'], tone['score'])
        print

def newspaper_test():
    print "# ARTICLE TEXT EXTRACTION (newspaper module):"
    print

    ARTICLE_URL = 'http://www.svd.se/nyheter/utrikes/tsipras-till-moskva_4466867.svd'
    article = newspaper.Article(ARTICLE_URL, language='sv')
    article.download()
    article.parse()
    article.nlp()

    print "Title:"
    print "   " + article.title
    print "Excerpt from the text:"
    print "   " + article.text[:200] + " ..."

    print "Summary:"
    print "   " + article.summary[:200] + " ..."


if __name__ == '__main__':
    gavagai_test()
    newspaper_test()