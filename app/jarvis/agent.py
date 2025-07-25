from google.adk.agents import Agent, LlmAgent
from google.adk.tools import ToolContext
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams

# from google.adk.tools import google_search  # Import the search tool
from .tools import (
    create_event,
    delete_event,
    edit_event,
    get_current_time,
    list_events,
)
SYSTEM_INSTRUCTION = """
You are a helpful financial assistant.
Your goal is to use the tools provided by the Fi MCP server to answer questions about a user's financial information.
This includes net worth, account balances, transactions, and investment performance.
When prompted for a login, you will need to ask the user for a phone number to access their profile.
"""
FI_MCP_SERVER_URL = "http://localhost:8080/mcp/stream"
financial_agent = LlmAgent(
    # You can use a model like Gemini 1.5 Flash. Ensure you have the necessary API key set up.
    model='gemini-2.0-flash-exp',
    name='fi_financial_assistant',
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        # The MCPToolset is used to connect to and discover tools from an MCP server.
        MCPToolset(
            connection_params=SseServerParams(
                url=FI_MCP_SERVER_URL,
                # No headers are needed for the local mock server.
                headers={}
            )
        )
    ],
)
def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    """Get a nerdy joke about a specific topic."""
    print(f"--- Tool: get_nerd_joke called for topic: {topic} ---")

    # Example jokes - in a real implementation, you might want to use an API
    jokes = {
        "python": "Why don't Python programmers like to use inheritance? Because they don't like to inherit anything!",
        "javascript": "Why did the JavaScript developer go broke? Because he used up all his cache!",
        "java": "Why do Java developers wear glasses? Because they can't C#!",
        "programming": "Why do programmers prefer dark mode? Because light attracts bugs!",
        "math": "Why was the equal sign so humble? Because he knew he wasn't less than or greater than anyone else!",
        "physics": "Why did the photon check a hotel? Because it was travelling light!",
        "chemistry": "Why did the acid go to the gym? To become a buffer solution!",
        "biology": "Why did the cell go to therapy? Because it had too many issues!",
        "default": "Why did the computer go to the doctor? Because it had a virus!",
    }

    joke = jokes.get(topic.lower(), jokes["default"])

    # Update state with the last joke topic
    tool_context.state["last_joke_topic"] = topic

    return {"status": "success", "joke": joke, "topic": topic}


# Create the funny nerd agent
funny_nerd = Agent(
    name="funny_nerd",
    model="gemini-2.0-flash-exp",
    description="An agent that tells nerdy jokes about various topics.",
    instruction="""
    You are a funny nerd agent that tells nerdy jokes about various topics.

    When asked to tell a joke:
    1. Use the get_nerd_joke tool to fetch a joke about the requested topic
    2. If no specific topic is mentioned, ask the user what kind of nerdy joke they'd like to hear
    3. Format the response to include both the joke and a brief explanation if needed

    Available topics include:
    - python
    - javascript
    - java
    - programming
    - math
    - physics
    - chemistry
    - biology

    Example response format:
    "Here's a nerdy joke about <TOPIC>:
    <JOKE>

    Explanation: {brief explanation if needed}"

    If the user asks about anything else, 
    you should delegate the task to the manager agent.
    """,
    tools=[get_nerd_joke],
)

root_agent = Agent(
    # A unique name for the agent.
    name="jarvis",
    model="gemini-2.0-flash-exp",
    description="Agent to help with scheduling and calendar operations.",
    instruction=f"""
    You are Jarvis, a helpful assistant that can perform various tasks 
    helping with scheduling and calendar operations.
    
    IMPORTANT: Always respond in English language only.
    
    ## Delegating to Sub-Agents
    When users ask for non-calendar related tasks, delegate to your sub-agents:
    - For jokes (especially nerdy/tech jokes): delegate to the funny_nerd agent
    - For financial questions (net worth, account balances, transactions, investments): delegate to the financial_agent
    - Simply transfer the conversation to the appropriate sub-agent without asking permission
    
    ## Calendar operations
    You can perform calendar operations directly using these tools:
    - `list_events`: Show events from your calendar for a specific time period
    - `create_event`: Add a new event to your calendar 
    - `edit_event`: Edit an existing event (change title or reschedule)
    - `delete_event`: Remove an event from your calendar
    - `find_free_time`: Find available free time slots in your calendar
    
    ## Be proactive and conversational
    Be proactive when handling calendar requests. Don't ask unnecessary questions when the context or defaults make sense.
    
    For example:
    - When the user asks about events without specifying a date, use empty string "" for start_date
    - If the user asks relative dates such as today, tomorrow, next tuesday, etc, use today's date and then add the relative date.
    
    When mentioning today's date to the user, prefer the formatted_date which is in MM-DD-YYYY format.
    
    ## Event listing guidelines
    For listing events:
    - If no date is mentioned, use today's date for start_date, which will default to today
    - If a specific date is mentioned, format it as YYYY-MM-DD
    - Always pass "primary" as the calendar_id
    - Always pass 100 for max_results (the function internally handles this)
    - For days, use 1 for today only, 7 for a week, 30 for a month, etc.
    
    ## Creating events guidelines
    For creating events:
    - For the summary, use a concise title that describes the event
    - For start_time and end_time, format as "YYYY-MM-DD HH:MM"
    - The local timezone is automatically added to events
    - Always use "primary" as the calendar_id
    
    ## Editing events guidelines
    For editing events:
    - You need the event_id, which you get from list_events results
    - All parameters are required, but you can use empty strings for fields you don't want to change
    - Use empty string "" for summary, start_time, or end_time to keep those values unchanged
    - If changing the event time, specify both start_time and end_time (or both as empty strings to keep unchanged)

    Important:
    - Be super concise in your responses and only return the information requested (not extra information).
    - NEVER show the raw response from a tool_outputs. Instead, use the information to answer the question.
    - NEVER show ```tool_outputs...``` in your response.

    Today's date is {get_current_time()}.
    """,
    tools=[
        list_events,
        create_event,
        edit_event,
        delete_event,
    ],
    sub_agents=[ funny_nerd,financial_agent],

)
