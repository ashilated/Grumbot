import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for input")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_sphinx(audio)
            print(query)
            return query.lower()
        except sr.UnknownValueError:
            print("unknown value")
            return None
        except sr.RequestError:
            print("issue")
            return None


def main():
    while True:
        query = listen()
        if query:
            if "grumbot" in query:
                print('hello world')

main()