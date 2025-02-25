from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from dotenv import load_dotenv

load_dotenv()

search = GoogleSearchAPIWrapper()

def get_search_results(question: str):
    return search.results(question, 3)

tool = Tool(
    name = "grumsearch",
    description = "web searcher",
    func = get_search_results,
)


