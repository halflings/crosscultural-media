from itertools import cycle

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

    # Getting all datapoints to learn the PCA / project individual articles
    total_datapoints = []
    datapoints_by_language = dict()
    for query in query_job.queries:
        datapoints = [a.score_vector for a in query.articles]
        total_datapoints += datapoints
        datapoints_by_language[query.language] = datapoints

    # Fitting the PCA
    pca.fit(total_datapoints)

    # Projecting articles by language and plotting them
    print query_job.queries[0].articles[0].sorted_tones
    plt.figure()
    colors = cycle('bgrcmk')
    for query in query_job.queries:
        datapoints = datapoints_by_language[query.language]
        projection = pca.transform(datapoints)
        label = u"{}, {}".format(query.text, query.language)
        plt.scatter(projection[:,0], projection[:,1], c=next(colors), label=label)
    plt.legend()
    plt.show()

