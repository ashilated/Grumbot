from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from search import get_search_results
import time
import prompts
import weather
import requests

model = OllamaLLM(model="gemma2:2b")

def chain(prompt):
    return ChatPromptTemplate.from_template(prompt) | model


def check_internet_connection():
    try:
        requests.head("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        print("Please connect me to the internet for this feature")
        return False

def check_to_search(question, history):
    c = chain(prompts.search_query)

    result = c.invoke({"question": question, "history": history})
    print(result)
    if "True" in result:
        return True
    else:
        return False

def parse_search_results(question, results):
    c = chain(prompts.search_parser)

    return c.invoke({"question": question, "results": results})

def parse_weather_data(question, data):
    if data == -1: return "Sorry, I could not find the weather information.\n"

    c = chain(prompts.weather_parser)
    return c.invoke({"question": question, "temp": data["temp"], "weather": data["weather"]})

def handle_conversation():
    history = ""
    c = chain(prompts.generic)

    while True:
        question = input("You: ")

        if any(word in question.lower() for word in ("weather", "temp", "temperature")):
            if not check_internet_connection(): break
            
            location = None
            if "in" in question.lower():
                location = question.split(" in ")[1]

            if "tomorrow" in question.lower():
                pass
                # result = parse_weather_data(question, weather.get_forecast(2, location))
            else:
                result = parse_weather_data(question, weather.get_current_weather(location))

        elif "time" in question.lower() and "date" in question.lower():
            result = time.strftime("It is %H:%M on %A, %B %d, %Y.\n")

        elif "time" in question.lower():
            result = time.strftime("It is currently %H:%M.\n")

        elif "date" in question.lower():
            result = time.strftime("Today is %A, %B %d, %Y.\n")

        elif "play bad apple" in question.lower():
            return 100

        elif not check_to_search(question, history):
            if not check_internet_connection(): break
            result = c.invoke({"history": history, "question": question})

        else:
            search_results = get_search_results(question)
            print(search_results)
            result = parse_search_results(question, search_results)

        history += f"\nUser: {question}\nAI: {result}"
        print("Grumbot: ", result)
        return result


