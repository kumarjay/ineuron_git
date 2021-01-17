import os, logging
from flask import Flask, request, render_template, jsonify
from twitter import TwitterClient

logging.basicConfig(filename='logging.log',
                    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level= logging.INFO)


app = Flask(__name__)

api = TwitterClient('Data')


# abc xyz

logger= logging.getLogger(__name__)

def strtobool(v):
    return v.lower() in ['yes', 'true', 't', 'l']


@app.route('/')
def index():
    logger.info('** Home page accessed **')
    logger.debug('** This is not debug **')
    return render_template('index.html')


@app.route('/tweets')
def tweets():
    logger.info('** Tweet page accessed **')
    logger.error('** This is the error **')
    retweets_only = request.args.get('retweets_only')
    api.set_retweet_checking(strtobool(retweets_only.lower()))
    with_sentiment = request.args.get('with_sentiment')
    api.set_with_sentiment(strtobool(with_sentiment.lower()))
    query = request.args.get('query')
    api.set_query(query)

    tweets = api.get_tweets()

    return jsonify({'data': tweets, 'count': len(tweets)})


port = int(os.environ.get('PORT', 8000))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
