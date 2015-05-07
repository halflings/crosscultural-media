import mongoengine


class QueryJob(mongoengine.Document):
    text = mongoengine.StringField(required=True)
    language = mongoengine.StringField(required=True)
    processed = mongoengine.BooleanField(default=False)

    def __str__(self):
        return u"<'{}' in '{}'>".format(self.text, self.language)


class Query(mongoengine.Document):
    text = mongoengine.StringField(required=True)
    language = mongoengine.StringField(required=True)
    source = mongoengine.ReferenceField(QueryJob)

    @property
    def articles(self):
        return Article.objects(query=self)


class Article(mongoengine.Document):
    query = mongoengine.ReferenceField(Query, required=True)
    title = mongoengine.StringField(required=True)
    text = mongoengine.StringField(required=True)

    @property
    def scores(self):
        return Score.objects(article=self)

    def build_scores(self, gavagai_resp):
        scores_data = gavagai_resp['texts'][0]
        for tone in sorted(scores_data['tonality'], key=lambda t: t['score'], reverse=True):
            Score(tone=tone['tone'], score=tone['score'], normalized_score=tone[
                  'normalizedScore'], article=self).save()

    @property
    def score_vector(self):
        return [score.normalized_score for score in sorted(self.scores, key=lambda s : s.tone)]


class Score(mongoengine.Document):
    tone = mongoengine.StringField(required=True)
    score = mongoengine.FloatField(required=True)
    normalized_score = mongoengine.FloatField(required=True)
    article = mongoengine.ReferenceField(Article)
