import telebot
import config
import json

from classes import User

bot = telebot.TeleBot(config.TOKEN)

def watchKarma(message):
	with open("user_list.json", "r") as f:
		arr_data = json.load(f)
		user_karma = arr_data[str(message.from_user.id)]["karma"]
		f.close()
	bot.send_message(message.chat.id, f"{message.from_user.first_name}, ваша карма: {user_karma}")

def asassessmentUser(message):
	if message.reply_to_message is not None:
		if message.text == "+":
			with open("user_list.json", "r") as fr:
					arr_data = json.load(fr)

					arr_data[str(message.reply_to_message.from_user.id)]["karma"] += 1

					with open("user_list.json", "w") as fw:
						json.dump(arr_data, fw, indent=4)
						fw.close()
						fr.close()

		elif message.text == "-":
			with open("user_list.json", "r") as fr:
					arr_data = json.load(fr)

					arr_data[str(message.reply_to_message.from_user.id)]["karma"] -= 1

					with open("user_list.json", "w") as fw:
						json.dump(arr_data, fw, indent=4)
						fw.close()
						fr.close()
		watchKarma(message)

@bot.message_handler(commands=['join'])
def joinKarma(message):

	def createUser(user_id, user_name):
		user = User(str(user_id), user_name)
		created_user = {str(user.user_id): {"username":user.user_name, "karma": user.karma}}
		with open("user_list.json", "w") as f:
			json.dump(created_user, f, indent=4)
			f.close()

	createUser(user_id=message.from_user.id, user_name=message.from_user.username)
	bot.send_message(message.chat.id, f"Пользователь {message.from_user.username} создан")

@bot.message_handler(commands=['help'])
def helpUser(message):
	if message.chat.type == 'private':
		bot.send_message(message.chat.id, "Test")
	else:
		bot.send_message(message.chat.id, "Перейдите в ЛС к боту")

@bot.message_handler(commands=["test"])
def testCheckAndOther(message):
	if message.from_user.id == 396224978:
		bot.send_message(message.chat.id, "Буду любить тебя кибер-папочка, Гуден =)")
		watchKarma(message)
	else:
		bot.send_message(message.chat.id, "Отвали, извращенец!")

@bot.message_handler(content_types=['text'])
def sendOutput(message):
	bot.send_message(message.chat.id, message.chat.type)
	if message.chat.type == 'group':
		
		if message.text == 'Карма':
			watchKarma(message)
		else:
			try:
				asassessmentUser(message)
			except:
				pass
# run

bot.polling(none_stop=True)