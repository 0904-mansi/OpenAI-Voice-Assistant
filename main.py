import speech_recognition as sr # machine's ability to listen to spoken words and identify them.
import pyttsx3 #text-to-speech conversion library
import openai
# api key
openai.api_key = "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"

#invoking the pyttsx3 init() factory function to get a reference to a pyttsx3.
engine = pyttsx3.init() 
#get the available voices
voices = engine.getProperty('voices')
# using the setProperty() method, we change the voice id accordingly to bring a male or female voice.
engine.setProperty('voices', voices[1].id)

# creating instance of speech_recognition module
r = sr.Recognizer()
#If device_index is unspecified or None then default audio source is used else it should between 0 - pyaudio.get_device_count() - 1
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "Mansi"
bot_name = "John"

while True:
    with mic as source:
        print("\n Listening...")
        # This function makes the necessary changes to the settings that allow the speech to be heard in a slightly noisy environment.
        r.adjust_for_ambient_noise(source)
        # listening 
        audio = r.listen(source)
    print("no longer listening")

    try:
        # recognizing the audio
        user_input = r.recognize_google(audio)
    except:
        continue
    
    prompt = user_name+":"+user_input + "\n"+bot_name+":"
    #print(prompt)
    conversation += prompt
    #print(conversation)
    
    
    response = openai.Completion.create(
        model="text-davinci-003", #ID of the model to use
        prompt=conversation,
        temperature=0.2, #Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
        max_tokens=256, #The maximum number of tokens to generate in the completion.
        top_p=1, #top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        frequency_penalty=0, #decrease the model's likelihood to repeat the same line.
        presence_penalty=0 # increasing the model's likelihood to talk about new topics.
    )

    #taking a response from a chatbot and cleans it up by removing any new line characters ("\n") 
    #and filtering out any part of the response that comes after the chatbot's or user's name.
    response_str = response["choices"][0]["text"].replace("\n", "")
    # The [0] index is used to retrieve only the first part of the split text, 
    # which is the part of the response that comes before the user's or chatbot's name.
    response_str =response_str.split(
        user_name + ":" ,1)[0].split(bot_name+ ":",1)[0]

    conversation+= response_str +"\n"
    #print(conversation)
   
    engine.say(response_str)
    print(response_str)
    engine.runAndWait()
