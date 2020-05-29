import telebot
import config
import json

from classes import User

bot = telebot.TeleBot(config.TOKEN)



def watchUserKarma(message):
	with open("user_list.json", "r") as f:
		arr_data = json.load(f)
		user_karma = arr_data[str(message.from_user.id)]["karma"]
		f.close()

	if message.reply_to_message is not None:
		bot.send_message(message.chat.id, f"{message.reply_to_message.from_user.first_name}, ваша карма: {user_karma}")
	else:
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
			watchUserKarma(message)

		elif message.text == "-":
			with open("user_list.json", "r") as fr:
					arr_data = json.load(fr)

					if arr_data[str(message.reply_to_message.from_user.id)]["karma"] >= -10:
						arr_data[str(message.reply_to_message.from_user.id)]["karma"] -= 1
					else:
						arr_data[str(message.reply_to_message.from_user.id)]["karma"] == 0
						bot.send_message(message.id, "Выдано предупреждение")

					with open("user_list.json", "w") as fw:
						json.dump(arr_data, fw, indent=4)
						fw.close()
						fr.close()
			watchUserKarma(message)

@bot.message_handler(commands=['allKarma'])
def wathGlobalKarma(message):
	try:
		with open("user_list.json", "r") as f:
			arr_data = json.load(f)
			for user in arr_data:

				user_info = arr_data[user]
				bot.send_message(message.chat.id, f"У пользователя {user_info['user_firts_name']}: {user_info['karma']} кармы.")
				
			f.close()
	except:
		pass

@bot.message_handler(commands=['join'])
def joinKarma(message):

	def createUser(user_id, user_name, user_firts_name):
		user = User(user_id, user_name, user_firts_name)
		created_user = {str(user.user_id): {"username":user.user_name, "user_firts_name":user.user_firts_name,  "karma": user.karma}}	# create user model

		with open("user_list.json") as fa:		# update json data
			arr_date = json.load(fa)
			arr_date.update(created_user)

			with open("user_list.json", "w") as fw:	# dump json data in file
				json.dump(arr_date, fw)
				fw.close()
				fa.close()

	createUser(user_id=message.from_user.id, user_name=message.from_user.username, user_firts_name=message.from_user.first_name)
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
		watchUserKarma(message)
	else:
		bot.send_message(message.chat.id, "Отвали, извращенец!")

@bot.message_handler(content_types=['text'])
def sendOutput(message):
	if message.chat.type == 'group' or message.chat.type == "supergroup":
		
		if message.text.lower() == 'карма':
			watchUserKarma(message)
		else:
			try:
				asassessmentUser(message)
			except:
				pass
# run

bot.polling(none_stop=True)