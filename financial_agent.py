from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch
from os import getenv
from dotenv import load_dotenv

load_dotenv()

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
    instructions="Use tables to display the data",
    show_tool_calls=True,
    markdown=True,
)

multi_ai_agent = Agent(
    name="Stock market agent",
    role="A comprehensive assistant specializing in stock market analysis by combining financial insights with real-time web searches to deliver accurate, up-to-date information",
    team=[web_search_agent, finance_agent],
    model=Groq(api_key=getenv("GROQ_API_KEY"), id="llama3-groq-8b-8192-tool-use-preview"),
    instructions=["Always include sources", "Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,
)

multi_ai_agent.print_response("Compare the performance of the Nvidia Stock with its competitors in the year 2023", stream=True)
