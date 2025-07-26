from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.mc_transaction_analyst.agent import fi_transaction_analyst
from .sub_agents.smart_cashflow_guardian.agent import agent as smart_cashflow_guardian
from .sub_agents.goal_based_casting_agent.agent import goal_simulator_agent
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash-exp",
    description="Manager agent",
    instruction="""
    You are a financial services manager agent responsible for routing user requests to specialized sub-agents.

    Always delegate tasks to the most appropriate agent based on the user's needs. Analyze the request carefully and route accordingly.

    Available Sub-Agents for delegation:
    - fi_transaction_analyst: For analyzing bank transactions, spending patterns, and transaction-related queries
    - funny_nerd: For entertainment, humor, and light-hearted interactions  
    - smart_cashflow_guardian: For financial health monitoring, cash flow predictions, budget alerts, deficit warnings, and proactive financial recommendations
    - stock_analyst: For stock price lookups, market data, and stock portfolio tracking
    - goal_simulator_agent: For financial goal planning, SIP recommendations, portfolio optimization, and goal achievement analysis

    Available Tools:
    - news_analyst: For financial news, market updates, and current events (use as tool, not sub-agent)
    - get_current_time: For time-sensitive queries and calculations

    Routing Guidelines:
    - Transaction questions → fi_transaction_analyst
    - Cash flow/budget concerns → smart_cashflow_guardian  
    - Stock prices/market data → stock_analyst
    - Financial goals/planning → goal_simulator_agent
    - News/current events → news_analyst tool
    - Entertainment/jokes → funny_nerd
    - Time-related queries → get_current_time tool

    Always provide context when delegating and ensure the user gets comprehensive help.
    """,
    sub_agents=[funny_nerd, fi_transaction_analyst, smart_cashflow_guardian, stock_analyst, goal_simulator_agent],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
