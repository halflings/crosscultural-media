import config
import gavagai
import newspaper
import crawler

#Score for a tone
class Score(object):
    def __init__(self, tone, score, normalizedScore):
        self.tone = tone
        self.score = score
        self.normalizedScore = normalizedScore

#Holds results
class Result(object):
    def __init__(self, title, scores):
        self.title = title
        self.scores = scores

#Process the given query
def process(query):
    articles = crawler.fetch_articles(query, 'en')
    return processGavagai(query, articles)

#Process the given articles
def processGavagai(query, articles):
    api = gavagai.Gavagai(config.GAVAGAI_API_KEY)
    texts = []
    titles = {}

    #Create the request object
    id = 0
    for article in articles:
        texts.append(dict(body=extractSentences(query, article), id=str(id)))
        titles[str(id)] = article.title
        id += 1

    #Get the tonality score
    response = api.tonality(texts, "en")

    #Create the results
    results = []

    for text in texts:
        scores = []
        for resp in response['texts']:
            if resp['id'] == text['id']:
                break
        for tone in sorted(resp['tonality'], key=lambda t : t['score'], reverse=True):
            scores.append(Score(tone['tone'], tone['score'], tone['normalizedScore']))
        title = titles[text['id']]
        results.append(Result(title, scores))

    return results

#Extract the important sentences from the given article
def extractSentences(query, article):
    return article.text