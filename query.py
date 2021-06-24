import datetime
import requests
from bs4 import BeautifulSoup

def findReservation(username):
    topics = {}
    timeline = api.user_timeline(screen_name=username, count=100)
    tweets_for_csv = [tweet.text for tweet in timeline]
    # Traverse through the first 100 tweets
    for latest_tweet in tweets_for_csv:
        bow_vector = dictionary.doc2bow(preprocess(latest_tweet))
        for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1 * tup[1]):
            topic = lda_model.print_topic(index, 5)
            if topic in topics:
                topics.update({topic: topics.get(topic) + score.item()})
            else:
                topics.update({topic: score.item()})
    sorted_topics = {k: v for k, v in sorted(topics.items(), key=lambda item: item[1], reverse=True)}
    return sorted_topics