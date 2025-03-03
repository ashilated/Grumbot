import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening for input")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_vosk(audio)
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
                print("your question is" + query.split("grumbot "[1]))

main()