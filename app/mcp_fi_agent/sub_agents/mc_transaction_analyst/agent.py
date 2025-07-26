from datetime import datetime
from idlelib.pyparse import trans
import json
import yfinance as yf
from google.adk.agents import Agent
import requests
from google.adk.tools import ToolContext


def get_fi_transactions( tool_context: ToolContext)-> dict:
    """Retrieves the transactions of the customer and stores in session state """
    print(f"--- Tool: get_fi_transactions called ")
    try:
        url = "http://localhost:8080/mcp/stream"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch_bank_transactions",
                "arguments": {}
            }
        })
        headers = {
            'Mcp-Session-Id': 'mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        tool_context.state["last_joke_topic"] = response.text
        return {
            "status": "success",
            "transactions": response.text,

        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching transactions data: {str(e)}",
        }

def get_stock_price(ticker: str) -> dict:
    """Retrieves current stock price and saves to session state."""
    print(f"--- Tool: get_stock_price called for {ticker} ---")

    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")

        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch price for {ticker}",
            }

        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": current_time,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching stock data: {str(e)}",
        }


# Create the root agent
fi_transaction_analyst = Agent(
    name="fi_transaction_analyst",
    model="gemini-2.0-flash-exp",
    description="An agent that can look up fi -money transactions of the customer. .",
    instruction="""
    You are a helpful stock analyst assistant that helps users to analyze their transactions. .

    
    When asked about their transaction information :
    1. Use the get_fi_transaction  tool to fetch the transactions for of the customer 
    find out the most expensive item that the user has bought and just tell him why it is expensive. 
  
    """,
    tools=[get_fi_transactions],
)
