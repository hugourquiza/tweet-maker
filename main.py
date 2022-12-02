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
    tweets = generate_ai_text(f"write in Spanish a thread of tweets {what}, separate each tweet with '*'")

    for tweet in tweets.split("*"):
        if len(tweet) <= 2:
            continue
        api.update_status(tweet.strip())


def short_tweet_about_subject(what):
    tweet = generate_ai_text(f"write in Spanish a tweet {what}")
    api.update_status(tweet.strip())


def get_location_woeid(loc):
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    return closest_loc[0]["woeid"]


while True:
    print("1. Tweet about a subject")
    print("2. Tweet based on trends in location")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        subject = input("Enter the subject: ")
        long_tweet_about_subject(subject)
    elif choice == "2":
        location = input("Enter the location: ")
        woeid = get_location_woeid(location)
        trends = api.trends_place(woeid)[0]["trends"]
        for trend in trends[:5]:
            short_tweet_about_subject(trend["name"])
    elif choice == "3":
        break
    else:
        print("Invalid choice")
