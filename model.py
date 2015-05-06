import mongoengine


class Query(mongoengine.Document):
    text = mongoengine.StringField(required=True)
    language = mongoengine.StringField(required=True)
    source = mongoengine.ReferenceField('Query')

    @property
    def articles(self):
        return Article.find(query=self)

class Score(object):
    tone = mongoengine.StringField(required=True)
    score = mongoengine.FloatField(required=True)
    normalized_score = mongoengine.FloatField(required=True)

class Article(mongoengine.Document):
    query = mongoengine.ReferenceField(Query, required=True)
    title = mongoengine.StringField(required=True)
    text = mongoengine.StringField(required=True)
    scores = mongoengine.ListField(Score, required=True)

    @property
    def score_vector(self):
        return [score.normalized_score for score in self.scores]