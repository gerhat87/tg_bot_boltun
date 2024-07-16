import telebot
from gtts import gTTS
import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

API_TOKEN = '7300624117:AAHYv75aHtujsNF02qxLuzyqCcqGDH9m3l4'
bot = telebot.TeleBot(API_TOKEN)

conversation_history = [
    {"role": "system", "content": "Ты вежливый, тактичный, внимательный консультант."}
]


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    conversation_history.append({"role": "user", "content": user_input})

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=conversation_history
    )

    ai_response_content = chat_completion.choices[0].message.content

    bot.send_message(message.chat.id, ai_response_content)

    tts = gTTS(text=ai_response_content, lang='ru')
    audio_file = 'voice_message.ogg'
    tts.save(audio_file)

    if os.path.exists(audio_file):
        with open(audio_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio)

        os.remove(audio_file)

    conversation_history.append({"role": "system", "content": ai_response_content})


bot.polling(none_stop=True)