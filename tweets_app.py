from flask import Flask, render_template, request, url_for, redirect
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
import pandas as pd
pd.set_option('display.max_colwidth', -1)

vader = SentimentIntensityAnalyzer()

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/result', methods=['POST'])
def result():
    raw_input= [x for x in request.form.values()]
    #text= [raw_text]
    print(raw_input)


    consumerKey = 'VsyMctyRBOnED0LBs3p6god55'
    consumerSecret = '8QLZGdnvyR4tqGJXsYgux574JiiiMb2SUgWecBectWApQVEZfk'
    accessToken = '783919955607560192-XMnzqtx7E7ggihOBdcaQKUtEKX9oTu7'
    accessTokenSecret = 'z85SZocmC8kQMlFa34XiY7KJcdjxVhokCcHhYwx4KWd8s'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    # input for term to be searched and how many tweets to search
    searchTerm = str(raw_input[0])
    NoOfTerms = int(raw_input[1])
    date_since = str(raw_input[2])

    tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en", since=date_since).items(NoOfTerms)


    neg_tweets=0
    neu_tweets=0
    pos_tweets=0

    tweets_results_df = pd.DataFrame(columns= ['Overall', 'Negative', 'Neutral', 'Positive', 'Tweet' ])
    tweets_results=[]
    for tweet in tweets:
        
        sentiment_result= vader.polarity_scores(tweet.text)
        compound_value = sentiment_result['compound']
        if compound_value >= 0.05:
            overall_value= "Positive"
            pos_tweets += 1
        elif compound_value <= -0.05:
            overall_value= "Negative"
            neg_tweets += 1
        else:
            overall_value= "Neutral"
            neu_tweets += 1
        tweets_results.append([overall_value, round(sentiment_result['neg']*100,2), round(sentiment_result['neu']*100,2), round(sentiment_result['pos']*100,2),tweet.text ])   

    tweets_results_df = pd.DataFrame(tweets_results, columns= ['Overall', 'Negative', 'Neutral', 'Positive', 'Tweet' ])
    
    return render_template('home.html',
                           neg_tweets= neg_tweets,
                           neu_tweets= neu_tweets,
                           pos_tweets= pos_tweets,
                           tables=[tweets_results_df.to_html(header="true")],
                           keyword= searchTerm,
                           NoOfTerms=NoOfTerms,
                           date_since=date_since
                           )




if __name__ == '__main__':
    app.run(debug=True)









    
