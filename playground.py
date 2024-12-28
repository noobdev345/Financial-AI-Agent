from dotenv import load_dotenv
from os import getenv
import phi.api
from phi.agent import Agent 
from phi.model.groq import Groq 
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch
from phi.playground import Playground, serve_playground_app

load_dotenv()

phi.api = getenv("PHI_API_KEY")

# web search agent
web_search_agent = Agent(
    name="web search agent",
    role="Search the web for the information",
    model=Groq(api_key=getenv("GROQ_API_KEY"), id="llama3-groq-8b-8192-tool-use-preview"),
    tools=[GoogleSearch(fixed_language="english", fixed_max_results=5)],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

# financial agent
finance_agent = Agent(
    name="finance agent",
    role="Provide financial insights",
    model=Groq(api_key=getenv("GROQ_API_KEY"), id="llama3-groq-8b-8192-tool-use-preview"),
    tools=[YFinanceTools(
        stock_price=True, 
        analyst_recommendations=True, 
        stock_fundamentals=True, 
        company_news=True)],
    instructions=["Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,
)

app = Playground(agents = [finance_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
