from itertools import cycle

import mongoengine
#import matplotlib.pyplot as plt
import sklearn.decomposition

import config
from crawler import enqueue_query, process_query

import sys

# Converts the 'array' type returned from pca.transform to a Python array
def toArray(projection):
    data = []
    for projPoint in projection:
        point = []
        for comp in projPoint:
            point.append(comp)
        data.append(point)
    return data

# Projects data points for all languages in the given query
def project(query_job):
    pca = sklearn.decomposition.PCA(2)

    # Getting all datapoints to learn the PCA / project individual articles
    total_datapoints = []
    datapoints_by_language = dict()
    for query in query_job.queries:
        datapoints = [a.score_vector for a in query.articles]
        total_datapoints += datapoints
        datapoints_by_language[query.language] = datapoints

    print >> sys.stderr,len(total_datapoints)

    # Fitting the PCA
    pca.fit(total_datapoints)

    # Projecting articles by language
    results = []
    for query in query_job.queries:
        datapoints = datapoints_by_language[query.language]
        projection = pca.transform(datapoints)
        results.append(dict(query=query.text, language=query.language, results=toArray(projection)))

    return results

def get_results(query, language):
    db = mongoengine.connect(config.db_name)
    db.drop_database(config.db_name)

    query_job = enqueue_query(query, language)
    process_query(query_job)

    return project(query_job)

if __name__ == '__main__':
    print get_results('coffee', 'en')
