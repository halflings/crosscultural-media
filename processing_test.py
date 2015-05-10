import mongoengine
import matplotlib.pyplot as plt
import sklearn.decomposition

import config
from crawler import enqueue_query, process_query

if __name__ == '__main__':
    db = mongoengine.connect(config.db_name)
    db.drop_database(config.db_name)

    query_job = enqueue_query('coffee', 'en')
    process_query(query_job)

    pca = sklearn.decomposition.PCA(2)
    total_datapoints = []
    datapoints_by_language = dict()
    for query in query_job.queries:
        datapoints = [a.score_vector for a in query.articles]
        total_datapoints += datapoints
        datapoints_by_language[query.language] = datapoints

    pca.fit(total_datapoints)

    print query_job.queries[0].articles[0].sorted_tones
    f, axes = plt.subplots(len(query_job.queries), sharex=True, sharey=True)
    for query, axis in zip(query_job.queries, axes):
        datapoints = datapoints_by_language[query.language]
        projection = pca.transform(datapoints)
        axis.scatter(projection[:,0], projection[:,1])
        axis.set_title(u"'{}' in '{}'".format(query.text, query.language))
    plt.show()

