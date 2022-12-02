import os
from time import sleep

import geocoder
import openai
import tweepy
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
auth = tweepy.OAuthHandler(os.environ.get("TWITTER_KEY"), os.environ.get("TWITTER_SECRET"))
auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN"), os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth, wait_on_rate_limit=True)


def generate_ai_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
    )
    return response['choices'][0]['text']


def long_tweet_about_subject(what):
    tweets = generate_ai_text(f"write in a Spanish a series of twits {what}, separate each twit with '*'")

    for tweet in tweets.split("*"):
        if len(tweet) <= 2:
            continue
        api.update_status(tweet.strip())
        sleep(30)


def short_tweet_about_subject(what):
    tweet = generate_ai_text(f"write in a Spanish a twit {what}")
    api.update_status(tweet.strip())


def get_location_woeid(loc):
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    return closest_loc[0]["woeid"]


trends = api.get_place_trends(get_location_woeid("Argentina"))


twitted_trends_count = 0
for trend in trends[0]['trends']:
    short_tweet_about_subject("explaining {}, using hashtags".format(trend['name']))
    twitted_trends_count += 1
    if twitted_trends_count > 5:
        break
