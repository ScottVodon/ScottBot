#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAADPR1PI9dkBALZAJMEBPsokltmQCyqgjiryQiMTb6gyfLxEsDMmtstOo8ZBhOMK1UP5LkC8xMQn48y7yKUz2IDyWIPSkHEGnPCZC1mx6mkyUX1pYrZCanzTKM2Rtwu5oZCE6oYSNCuOHe7m8QrIxtE4ZCKnqZCbslLz5KDOffGlgZDZD'
VERIFY_TOKEN = 'a3fg56qw34122'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                _message = message['message']['text'].upper()
                if _message == "I LOVE YOU":
                    response_sent_text = "I love you too"
                    send_message(recipient_id, response_sent_text)
                elif _message == "HELLO" or _message == "HI" or _message == "HEY":
                    response_sent_text = "Hello there"
                    send_message(recipient_id, response_sent_text)
                elif _message == "WHAT IS THE ANSWER TO LIFE, THE UNIVERSE AND EVERYTHING?":
                    response_sent_text = "42"
                    send_message(recipient_id, response_sent_text)
                elif _message == "I MISS YOU":
                    response_sent_text = "I miss you too, so does real Scott"
                    send_message(recipient_id, response_sent_text)
                elif _message == "TEST":
                    response_sent_text = "Test complete, I'm working!"
                    send_message(recipient_id, response_sent_text)


                elif message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                elif message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
                else:
                    response_sent_nontext = "Error, please tell real Scott I failed :("
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["have a great day!", "You are stunning!", "We're proud of you.",
    "Keep on being you!", "We're grateful to know you :)", "You rock!", "Looking good!",
    "have a great day!", "You're doing such a great job!", "We're cheering for you!", "Hey you! Smile!",
    "<(“)", ":D"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
