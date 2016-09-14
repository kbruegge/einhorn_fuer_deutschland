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
    # 'alternative':['Glitzer', 'Bananen'],
    'spitzenkandidat': ['Tinder Date'],
    'spitzenkandidaten': ['Tinder Dates'],
    'islamisten' :['Piraten', 'Faschisten', 'AfD Mitglieder'],
    'asylmissbrauch': ['Robbenbaby', 'Robbenkloppen'],
    'asylbewerber': ['Süße Gummibärchen', 'Bärchis <3'],
    'quote' : ['Torte'],
    'ausländer':['Einhörner'],
    'von storch':['vom Strauch', 'der Storch'],
    'wirtschaft':['Raumfahrt', 'Klassenfahrt'],
    'deutschland':['Schland', 'Lummerland'],
    'schande' :['Sahne'],
    'migranten' : ['Passanten'],
    'grenze' : ['Hose'],
    'flüchtlinge' : ['Spätzle', 'Freunde'],
    '#merkel' : ['#MettIgel', '#MerktNix'],
    'merkel' : ['Mutti', 'Mama'],
    'soldaten' : ['Legofiguren', 'Pizzalieferanten'],
    'bundeswehr' : ['Nationalmanschaft'],
    'afd-mitglieder':['Männerchor','Stadtmusikanten'],
    'wahrheit':['Schoki'],
    'kinder':['Rinder',],
    'schützen':['stürzen', 'schubsen'],
    'gauland':['Bauland', 'der geht nochn Meter', 'Sauland', 'Stauland'],
    'alternativefuer.de':['hasshilft.de'],
    'asylpolitik':['Zirkuszelte'],
    'linken' : ['Rechten'],
    'rechtsstaat' : ['Kartoffelsalat'],
    'ausländisch' : ['heimisch'],
    'imame' : ['Zuckerbäcker', 'Zombies'],
    '#npd' : ['#sexindustrie'],
    '#ungarn' : ['#FrauMalzahn'],
    'minderjährige' : ['Kaugummis', 'Zombies'],
    'massenzuwanderung' : ['Krieg der Sterne'],
    'gender' : ['Piepmatz', 'Willi in der Buchse'],
    'lösegeld' : ['Schokopudding'],
    'integration' : ['Hüpfburg'],
    'linksradikalen' : ['besorgte Bürger'],
}

dict_of_jerks = {
    'petry' : ['Petri Heil'],
    'holm' : ['Strohhalm'],
    'pazderski' : ['Panzertape'],
    'hampel' : ['Hampelmann'],
    'meuthen' : ['Mutantenkönig', 'Mupfelkönig'],
}

bullshit_pattern = re.compile('|'.join(dict_of_bullshit.keys()), re.IGNORECASE)
jerks_pattern = re.compile('|'.join(dict_of_jerks.keys()), re.IGNORECASE)


most_recent_status_ids = {}

def substituion(match, dict_of_replacements):
    try:
        replacement = random.choice(dict_of_replacements[match.group().lower()])
        return replacement
    except KeyError:
        print('Error!')


def fck_afd():
    for u in ['AfD_Bund','AfD_Bayern', 'AfD_MV', 'AfD_Hessen', 'christianlueth','Wahlen_AfD_2016', 'AfDBerlin']:
        check_tweets_for_bullshit(user=u)
        time.sleep(2)


def check_tweets_for_bullshit(user='AfD_Bund'):
    global most_recent_status_ids
    last_id = None

    if user in most_recent_status_ids:
        last_id = most_recent_status_ids[user]

    if last_id:
        bullshit_tweets = api.user_timeline(user, since_id=last_id)
    else:
        bullshit_tweets = api.user_timeline(user)
    if not bullshit_tweets:
        print('No Tweets found.')
        return

    most_recent_status_ids[user] = bullshit_tweets[0].id

    for tweet in bullshit_tweets:
        bullshit_text = bullshit_pattern.sub(lambda match: substituion(match, dict_of_bullshit), tweet.text)
        if bullshit_text != tweet.text:
            new_text = jerks_pattern.sub(lambda match: substituion(match, dict_of_jerks), bullshit_text)
            # if new_text != bullshit_text:
            #     print('replaced some names')
            new_text = new_text.replace('#AfD', '#EfD')
            #shorten text
            new_text = new_text[0:139]
            # print('id:   {} : original tweet:---- \n {} \n new tweet:------\n {}'.format(tweet.id, tweet.text, new_text))

            api.update_status('@{} {}'.format(user, new_text), in_reply_to_status_id=tweet.id)



def tweet_time_of_day():
    texts = [
        'Es ist 12:00. Die AFD stinkt immernoch. #einhornfuerdeutschland www.hasshilft.de',
        'Ich glaub es hackt! Besorgtes Einhorn macht sich sorgen über die Zukunft Deutschlands. #schland #einhornfuerdeutschland www.hasshilft.de',
        'Your daily "diese verkackten AFD rassisten werden immernoch gewählt" reminder. #einhornfuerdeutschland www.hasshilft.de',
        'Demnächst ist Wahl. Wählt das #einhornfuerdeutschland für eine bessere Zukunft! www.hasshilft.de',
        'Wir müssen die Zukunft unserer Kinder schützen! Wählt das #einhornfuerdeutschland! www.hasshilft.de',
        'Ayran für alle! #einhornfuerdeutschland #kbfr'
    ]
    api.update_status(random.choice(texts))

def main():

    schedule.every(10).minutes.do(fck_afd)
    schedule.every().day.at("12:00").do(tweet_time_of_day)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()
