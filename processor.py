import config
import gavagai
import newspaper
import crawler
import extractor
from json import JSONEncoder

#Score for a tone
class Score(object):
    def __init__(self, tone, score, normalizedScore):
        self.tone = tone
        self.score = score
        self.normalizedScore = normalizedScore

#Holds results for a sentence
class Sentence(object):
    def __init__(self, num, scores):
        self.num = num
        self.scores = scores

#Holds results
class Result(object):
    def __init__(self, title, sentences):
        self.title = title
        self.sentences = sentences

#JSON serializer
class ResultEncoder(JSONEncoder):
    def default(self, data):
        return data.__dict__

#Process the given query
def process(query):
    articles = crawler.fetch_articles(query, 'en')
    return process_gavagai(query, articles)

#Process the given articles
def process_gavagai(query, articles):
    api = gavagai.Gavagai(config.GAVAGAI_API_KEY)
    texts = []
    results = []
    sentences = {}

    #Create the request object
    articleId = 0
    sentenceId = 0
    for article in articles:
        for sentence in extract_sentences(article, query):
            texts.append(dict(body=sentence, id=str(sentenceId)))
            sentences[str(sentenceId)] = articleId
            sentenceId += 1

        results.append(Result(article.title, []))
        articleId += 1

    #Get the tonality score
    response = api.tonality(texts, "en")

    #Create the results
    for text in texts:
        scores = []
        for resp in response['texts']:
            if resp['id'] == text['id']:
                break
        for tone in sorted(resp['tonality'], key=lambda t : t['score'], reverse=True):
            scores.append(Score(tone['tone'], tone['score'], tone['normalizedScore']))
        result = results[sentences[text['id']]]
        result.sentences.append(Sentence(len(result.sentences), scores))

    return results

#Extract the important sentences from the given article
def extract_sentences(article, query):
    return extractor.extract_surrounded_context(article.text, query)