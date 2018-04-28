import tweepy
import sys
from time import sleep
import os
import logging

from gif_functions import gifConcat
from giphy_functions import getRandomGifs
from sqlite_functions import create_table_if_exists,create_connection_file, insert_new_response, get_last_uid

# DATA
TW_CONSUMER_KEY = os.environ['TW_CONSUMER_KEY']
TW_CONSUMER_SECRET = os.environ['TW_CONSUMER_SECRET']
TW_ACCESS_TOKEN = os.environ['TW_ACCESS_TOKEN']
TW_ACCESS_TOKEN_SECRET = os.environ['TW_ACCESS_TOKEN_SECRET']

## RUN
auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
conn = create_connection_file('botlog.db')
create_table_if_exists(conn)

# Search and generate image
def composeImage(text = "latorre + batistuta"):
	terms = list(map(lambda x: x.strip(), text.split('+')))
	del terms[3:]
	ok = getRandomGifs(terms)
	final = gifConcat(terms)
	return final

#Upload file to tw
def mediaUpload(filename):
    try:
        response = api.media_upload(filename)
    except:
        print (sys.exc_info()[0])
        logging.exception('Media upload')
        return False
    return response.media_id_string

#a = api.mentions_timeline()

#uid = a[0].id
#what? fake uid

uid = get_last_uid(conn)

while(True):
    sleep(5)
    mentions = api.mentions_timeline(uid)
    print "Mention lenght = %d" %(len(mentions))
    for i in mentions:
        cleanText = i.text.replace("@git_play_bot","")
        for u in i.entities["user_mentions"]:
            cleanText = cleanText.replace("@"+u["screen_name"],"")
        m = "%s. By @%s. Via @giphy." %(cleanText, i.user.screen_name)
        img = composeImage(cleanText)
        mediaId = mediaUpload(img)
        medias = list()
        medias.append(mediaId)
        api.update_status(status=m, media_ids=medias, in_reply_to_status_id=i.id)
        uid = i.id
        rowid = insert_new_response(conn,uid,i.text,img)
        print rowid
