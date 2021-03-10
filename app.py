# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,VideoSendMessage,ImageSendMessage,
	SourceUser, SourceGroup, SourceRoom,
	TemplateSendMessage, ConfirmTemplate, MessageAction,
	ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
	PostbackAction, DatetimePickerAction,
	CameraAction, CameraRollAction, LocationAction,
	CarouselTemplate, CarouselColumn, PostbackEvent,
	StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
	ImageMessage, VideoMessage, AudioMessage, FileMessage,
	UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
	FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
	TextComponent, SpacerComponent, IconComponent, ButtonComponent,
	SeparatorComponent, QuickReply, QuickReplyButton
)

app = Flask(__name__)

# you can replace by load env file
handler = WebhookHandler('96a78c75071f85c5766b60b0342932e3') 
line_bot_api = LineBotApi('oPgMn4WLvlT7j9xJrVzkMHw0q45goo6KpRDdKYAVnApKMiJikZ9/mo9WhZ23SHCX737hawGiUS1drtQ7Tzk3IY3HJIznEXBWxrqkqxSmZrUUquRALLLTx4Mf2ASzOvxk1ncoosDaepZXdArmsAhPSgdB04t89/1O/w1cDnyilFU=') 


@app.route('/')
def index():
	return "<p>Hello World!</p>"

@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'


# ========== handle user message ==========
item = ''
@handler.add(MessageEvent, message=TextMessage)  
def handle_text_message(event):
	# message from user                  
	msg = event.message.text
	key_word = ['在','進入','查不到','顯示','軌跡','距離','GPS','gps']
	count = 0
	for k in key_word :
		if k in msg :
			count += 1
	if count >= 2 :		
		count = 0
		line_bot_api.reply_message(event.reply_token, msg)

		message = { "type":"postback",
					"label":"SignError",
					"data":"SignError",
					"displayText":"訊號異常：請輸入車號"
					}
		line_bot_api.reply_message(event.reply_token, message)

# @handler.add(PostbackEvent)
# def handle_postback(event) :
# 	global item
# 	item = event.postback.data
# 	if item == 'SignError' :



	


import os
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=os.environ['PORT'])
	
