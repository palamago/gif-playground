import tweepy
import sys
import time
import os
import logging

from gif_functions import composeImage
from sqlite_functions import create_table_if_exists,create_connection_file, insert_new_response, get_last_uid

# DATA
TW_CONSUMER_KEY = os.environ['GIF_TW_CONSUMER_KEY']
TW_CONSUMER_SECRET = os.environ['GIF_TW_CONSUMER_SECRET']
TW_ACCESS_TOKEN = os.environ['GIF_TW_ACCESS_TOKEN']
TW_ACCESS_TOKEN_SECRET = os.environ['GIF_TW_ACCESS_TOKEN_SECRET']

## RUN
auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
conn = create_connection_file('botlog.db')
create_table_if_exists(conn)



#Upload file to tw
def mediaUpload(filename):
    try:
        response = api.media_upload(filename)
        return response.media_id_string
    except Exception as e: raise
    return False

#RUN
logging.basicConfig(filename="gif_playground.log",
                    format='%(asctime)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

uid = get_last_uid(conn)

try:
    mentions = api.mentions_timeline(uid)
    log.info("Mentions: %d" %(len(mentions)))
    for i in mentions:
        start_time = time.time()
        cleanText = i.text.replace("@git_play_bot","")
        for u in i.entities["user_mentions"]:
            cleanText = cleanText.replace("@"+u["screen_name"],"")
        for h in i.entities["hashtags"]:
            cleanText = cleanText.replace(" #"+h["text"],"")
        m = "%s. By @%s. Via @giphy." %(cleanText, i.user.screen_name)

        img = ""
        if cleanText != "" and "+" in cleanText:
            img = composeImage(cleanText)
            mediaId = mediaUpload(img)
            medias = list()
            medias.append(mediaId)
            api.update_status(status=m, media_ids=medias, in_reply_to_status_id=i.id)

        uid = i.id
        rowid = insert_new_response(conn,uid,i.user.screen_name,i.text,img)
        log.info("%s: %s -> %s secs" % (uid,cleanText,round(time.time() - start_time)))
except Exception as e:
    log.exception(sys.exc_info()[0])
