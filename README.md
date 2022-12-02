This tiny app uses OpenAI API to generate and post tweets using a location trending topics.

To start tweeting:

Create a .env file where you must configure the following keys:
```
OPENAI_API_KEY
TWITTER_KEY
TWITTER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```

Then run:

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```
