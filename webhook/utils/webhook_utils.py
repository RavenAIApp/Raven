import os
import json
import requests

import openai
from django.conf import settings

class FBUtils:

    FB_POST_URL = "https://graph.facebook.com/v16.0/me/messages?access_token="
    FB_GRAPH_URL = "https://graph.facebook.com/v16.0/"
    FB_GROUP_URL = "https://graph.facebook.com/v16.0/"

    @staticmethod
    def send_text_message(receiver_id, msg):
        post_message_url = FBUtils.FB_POST_URL + settings.FB_ACCESS_TOKEN
        response_msg = json.dumps({"recipient": {"id":receiver_id}, "message": {"text": msg}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
        return status.json()

    @staticmethod
    def get_user_details(userid):
        # these are page scoped IDs - https://chatbotsmagazine.com/fb-messenger-bot-how-to-identify-a-user-via-page-app-scoped-user-ids-f95b807b7e46
        # http://stackoverflow.com/questions/40404524/fb-messenger-get-email-address-from-fbid
        fb_user_url = FBUtils.FB_GRAPH_URL + userid + "?access_token=" + settings.FB_ACCESS_TOKEN
        # print "User Details URL:", fb_user_url
        resp = requests.get(fb_user_url)
        if resp:
            return resp.json()
        else:
            return None

    @staticmethod
    def send_media_message(receiver_id, message_type, media_url):
        # https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment
        post_message_url = FBUtils.FB_POST_URL + settings.FB_ACCESS_TOKEN
        response_msg = json.dumps({"recipient": {"id": receiver_id}, "message": {"attachment": {"type": message_type,
                                                                                    "payload": {"url": media_url}}}})
        #print "-----> Sending:", response_msg
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
        return status.json()

    @staticmethod
    def get_group_feed(group_id):
        # https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment
        group_feed_url = FBUtils.FB_GROUP_URL + group_id + "/feed?access_token=" + settings.FB_ACCESS_TOKEN
        print(group_feed_url)
        resp = requests.get(group_feed_url)
        if resp:
            return resp.json()
        else:
            return None

class OpenAIUtils:

    openai.api_key = settings.OPENAI_API_KEY
    CHAT_MODEL = "text-davinci-003"
    EMBEDDING_MODEL = "ada-002"

    @staticmethod
    def simple_answer(question):
        completion = openai.Completion.create(model=OpenAIUtils.CHAT_MODEL, prompt=question)
        return completion.choices[0].text
