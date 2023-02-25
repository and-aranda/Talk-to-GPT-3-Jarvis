import openai
import pyttsx3
import speech_recognition as sr
import whisper
import json 

# openai
openai.api_key = proceess.env.OPENAI_API_KEY
model = whisper.load_model('base')
engine = pyttsx3.init()

# set engine
# MX =  com.apple.speech.synthesis.voice.juan
# US = com.apple.speech.synthesis.voice.Alex
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.juan')

r = sr.Recognizer()
mic = sr.Microphone(device_index=0)

# Set keyword to activate listening
keyword = "jarvis"

# Set threshold level (low value for low sensitivity, high value for high sensitivity)
threshold = 500

conversation = ""
user_name = "Andres"
bot_name = "Yarvis"

listening = False

with mic as source:
    r.adjust_for_ambient_noise(source, duration=0.5)

while True:
    if not listening:
        with mic as source:


            print("Say '{}' to start listening...".format(keyword))

            audio = r.listen(source)

        try:
            user_input = r.recognize_google(audio, language="es-MX")
            if user_input.lower() == keyword.lower():
                listening = True
                
                print("Escuchando...")
                engine.say("Preguntame algo, estoy escuchando.")
                engine.runAndWait()
        except sr.UnknownValueError:
            continue

    with mic as source:
        audio = r.listen(source)
        with open('output.wav', 'wb') as f:
            f.write(audio.get_wav_data())
    print("no longer listening.\n")
    try:
        output = model.transcribe('output.wav', fp16=False)
        user_input = output['text']
        print("user input : " + user_input)
    except Exception as e :
        print(e)
        continue
    
    prompt = user_name + ": " + user_input + "\n" + bot_name+ ": "
    
    conversation += prompt
    
    response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = conversation,
            max_tokens = 1024,
            n = 1,
            stop=[user_name+":"],
            temperature=0.2,
        )
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
    
    conversation += response_str + "\n"
    print(response_str)
    
    engine.say(response_str)
    engine.runAndWait()

