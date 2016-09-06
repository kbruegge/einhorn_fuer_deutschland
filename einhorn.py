import tweepy
import time
import schedule
import random
import re
import configparser

config = configparser.ConfigParser()
config.read('auth.ini')

auth = tweepy.OAuthHandler(config['AUTH']['auth_token'],config['AUTH']['auth_secret'])
auth.set_access_token(config['AUTH']['access_token'],config['AUTH']['access_secret'])

api = tweepy.API(auth)

dict_of_bullshit = {
    'alternative':['Glitzer', 'Bananen'],
    'islamisten' :['Piraten', 'Faschisten', 'AfD Mitglieder'],
    'asylmissbrauch': ['Robbenbabys', 'Robbenkloppen'],
    'quote' : ['Torte'],
    'petry' : ['Petri Heil'],
    'ausländer':['Einhörner'],
    'von Storch':['vom Strauch', 'der Storch'],
    'wirtschaft':['Raumfahrt', 'Klassenfahrt'],
    'deutschland':['Schland', 'Lummerland'],
    'schande' :['Sahne'],
    'migranten' : ['Passanten'],
    'grenze' : ['Hose'],
    'flüchtlinge' : ['Spätzle'],
    '#merkel' : ['#MettIgel', '#MerktNix'],
    'soldaten' : ['Legofiguren'],
    'bundeswehr' : ['Nationalmanschaft', 'Gurkentruppe'],
    'meuthen' : ['Mutantenkönig', 'Mupfelkönig'],
    'afd-mitglieder':['Männerchor','Stadtmusikanten'],
    'wahrheit':['Schoki'],
    'kinder':['Rinder',],
    'schützen':['stürzen', 'schubsen'],
    'gauland':['Bauland', 'der geht nochn Meter', 'Sauland', 'Stauland'],
    'alternativefuer.de':['hasshilft.de'],
    'asylpolitik':['Zirkuszelte'],
}

pattern = re.compile('|'.join(dict_of_bullshit.keys()), re.IGNORECASE)
most_recent_status_id = 773136476364210176

def substituion(match):
    try:
        # print('match: ' + match.group().lower())
        replacement = random.choice(dict_of_bullshit[match.group().lower()])
        # print('replacment: '  + replacement)
        return replacement
    except KeyError:
        print('Error!')



def check_tweets_for_bullshit(user='AfD_Bund'):
    global most_recent_status_id
    print(most_recent_status_id)
    if most_recent_status_id:
        bullshit_tweets = api.user_timeline(user, since_id=most_recent_status_id)
    else:
        bullshit_tweets = api.user_timeline(user)
    if not bullshit_tweets:
        print('No Tweets found.')
        return

    # print('latest id' + str(bullshit_tweets[-1].id))
    most_recent_status_id = bullshit_tweets[0].id
    for tweet in bullshit_tweets:
        new_text = pattern.sub(substituion, tweet.text)
        if new_text != tweet.text:
            print('id:   {} : original tweet:---- \n {} \n new tweet:------\n {}'.format(tweet.id, tweet.text, new_text))
            #shorten text
            new_text = new_text[0:(140-(len(user) + 2))]
            api.update_status('@{} {}'.format(user, new_text), in_reply_to_status_id=tweet.id)



def tweet_time_of_day(text='Es ist 12:00. Die AFD stinkt immernoch. #einhornfuerdeutschland'):
    api.update_status(text)

def main():

    schedule.every(2).minutes.do(check_tweets_for_bullshit)
    schedule.every().day.at("12:00").do(tweet_time_of_day)

    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == '__main__':
    main()
