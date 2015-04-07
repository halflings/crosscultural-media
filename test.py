import config
import gavagai

if __name__ == '__main__':
    api = gavagai.Gavagai(config.API_KEY)
    texts = [dict(body="I am angry, I hate you, blah blah, you're terrible.", id="angrytext"),
             dict(body="I am happy. Cats are cute, flowers smell good.", id="happytext"),
             dict(body="Stockholm is Sweden's capital. It isn't close to Beijing.", id="neutraltext"),]
    response = api.tonality(texts, "en")

    for text in texts:
        print "{} : {}".format(text['id'], text['body'])
        for resp in response['texts']:
            if resp['id'] == text['id']:
                break
        for tone in resp['tonality']:
            print "* {} = {}".format(tone['tone'], tone['score'])
        print