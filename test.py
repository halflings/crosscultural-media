import config
import gavagai
import newspaper

def gavagai_test():
    print "# GAVAGAI (gavagai module):"
    print

    api = gavagai.Gavagai(config.GAVAGAI_API_KEY)
    texts = [dict(body="I am angry, I hate you, blah blah, you're terrible.", id="angrytext"),
             dict(body="I am happy. Cats are cute, flowers smell good.", id="happytext"),
             dict(body="Stockholm is Sweden's capital. It isn't close to Beijing.", id="neutraltext"),]
    response = api.tonality(texts, "en")

    for text in texts:
        print "{} : {}".format(text['id'], text['body'])
        for resp in response['texts']:
            if resp['id'] == text['id']:
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