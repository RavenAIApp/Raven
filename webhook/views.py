import json

from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .utils.webhook_utils import FBUtils,  OpenAIUtils

# Create your views here.
def index(request):
    return render(request, "index.html")

def privacy(request):
    return render(request, "privacy_policy.html")

# Create your views here.
class WebHookView(generic.View):
    def get(self, request, *args, **kwargs):
        token_in = ""
        try:
            token_in = self.request.GET['hub.verify_token']
            if token_in == settings.FB_VERIFIED_TOKEN:
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse("Error, Invalid Token!")
        except Exception as error:
                return HttpResponse("Error, No Token!")
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    #sender info
                    #sender = message['sender']['id']
                    #user_details = FBUtils.get_user_details(sender)
                    #print(user_details)

                    # Print the message to the terminal
                    print(message)
                    result = OpenAIUtils.simple_answer(message['message']['text'])
                    FBUtils.send_text_message(message['sender']['id'], result)

        return HttpResponse()

def group_feed(request):
    group_id = "1193449958038942"
    feed_info = FBUtils.get_group_feed(group_id)
    return HttpResponse(feed_info)
