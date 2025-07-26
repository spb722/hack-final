from google.adk.tools import ToolContext
import json
import requests
import numpy as np
import math
def fetch_net_worth( tool_context: ToolContext)-> dict:
    """Retrieves the net_worth of the customer and stores in session state """
    print(f"--- Tool: get_fi_transactions called ")
    try:
        url = "http://localhost:8080/mcp/stream"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch_net_worth",
                "arguments": {}
            }
        })
        headers = {
            'Mcp-Session-Id': 'mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        tool_context.state["net_worth"] = response.text
        return {
            "status": "success",
            "transactions": response.text,

        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching net_worth data: {str(e)}",
        }


def fetch_credit_report( tool_context: ToolContext)-> dict:
    """Retrieves the credit_report of the customer and stores in session state """
    print(f"--- Tool: get_fi_transactions called ")
    try:
        url = "http://localhost:8080/mcp/stream"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch_credit_report",
                "arguments": {}
            }
        })
        headers = {
            'Mcp-Session-Id': 'mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        tool_context.state["credit_report"] = response.text
        return {
            "status": "success",
            "transactions": response.text,

        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching credit_report data: {str(e)}",
        }
def fetch_epf_details( tool_context: ToolContext)-> dict:
    """Retrieves the epf_details of the customer and stores in session state """
    print(f"--- Tool: get_fi_transactions called ")
    try:
        url = "http://localhost:8080/mcp/stream"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch_epf_details",
                "arguments": {}
            }
        })
        headers = {
            'Mcp-Session-Id': 'mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        tool_context.state["epf_details"] = response.text
        return {
            "status": "success",
            "transactions": response.text,

        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching transactions data: {str(e)}",
        }
def fetch_mf_transactions( tool_context: ToolContext)-> dict:
    """Retrieves the mutual_fund_transactions of the customer and stores in session state """
    print(f"--- Tool: get_fi_transactions called ")
    try:
        url = "http://localhost:8080/mcp/stream"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch_mf_transactions",
                "arguments": {}
            }
        })
        headers = {
            'Mcp-Session-Id': 'mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        tool_context.state["mf_transactions"] = response.text
        return {
            "status": "success",
            "transactions": response.text,

        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching transactions data: {str(e)}",
        }


def fetch_stock_transactions( tool_context: ToolContext)-> dict:
    """Retrieves the stock_transactions of the customer and stores in session state """
    print(f"--- Tool: get_fi_transactions called ")
    try:
        url = "http://localhost:8080/mcp/stream"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch_stock_transactions",
                "arguments": {}
            }
        })
        headers = {
            'Mcp-Session-Id': 'mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        tool_context.state["stock_transactions"] = response.text
        return {
            "status": "success",
            "transactions": response.text,

        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching stock_transactions data: {str(e)}",
        }

def fetch_bank_transactions( tool_context: ToolContext)-> dict:
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
        tool_context.state["bank_transactions"] = response.text
        return {
            "status": "success",
            "transactions": response.text,

        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching transactions data: {str(e)}",
        }
#---------------------------------------------------------------------------------
def calculate_current_portfolio_stats(tool_context: ToolContext) -> dict:
    """Calculates current portfolio statistics from user's financial data."""
    try:
        # Fetch all financial data
        net_worth_data = fetch_net_worth(tool_context)
        mf_data = fetch_mf_transactions(tool_context)
        epf_data = fetch_epf_details(tool_context)

        # Parse net worth data
        if net_worth_data.get("status") == "success":
            net_worth_response = json.loads(net_worth_data["transactions"])

            # Extract asset values
            assets = net_worth_response["netWorthResponse"]["assetValues"]
            total_net_worth = int(net_worth_response["netWorthResponse"]["totalNetWorthValue"]["units"])

            # Calculate asset breakdown
            asset_breakdown = {}
            for asset in assets:
                asset_type = asset["netWorthAttribute"]
                value = int(asset["value"]["units"])
                asset_breakdown[asset_type] = value

            # Calculate equity vs debt allocation
            equity_assets = (
                    asset_breakdown.get("ASSET_TYPE_MUTUAL_FUND", 0) +
                    asset_breakdown.get("ASSET_TYPE_INDIAN_SECURITIES", 0) +
                    asset_breakdown.get("ASSET_TYPE_US_SECURITIES", 0)
            )

            debt_assets = (
                    asset_breakdown.get("ASSET_TYPE_EPF", 0) +
                    asset_breakdown.get("ASSET_TYPE_SAVINGS_ACCOUNTS", 0)
            )

            equity_percentage = (equity_assets / total_net_worth * 100) if total_net_worth > 0 else 0
            debt_percentage = (debt_assets / total_net_worth * 100) if total_net_worth > 0 else 0

            result = {
                "status": "success",
                "total_net_worth": total_net_worth,
                "equity_assets": equity_assets,
                "debt_assets": debt_assets,
                "equity_percentage": round(equity_percentage, 2),
                "debt_percentage": round(debt_percentage, 2),
                "asset_breakdown": asset_breakdown
            }
            
            # Store in session state for future reference
            tool_context.state["portfolio_stats"] = result
            return result
        else:
            return {"status": "error", "error_message": "Failed to fetch net worth data"}

    except Exception as e:
        return {"status": "error", "error_message": f"Error calculating portfolio stats: {str(e)}"}


def estimate_monthly_income(tool_context: ToolContext) -> dict:
    """Estimates monthly income from bank transaction patterns."""
    try:
        bank_data = fetch_bank_transactions(tool_context)

        if bank_data.get("status") == "success":
            bank_response = json.loads(bank_data["transactions"])

            # Look for salary credits in transactions
            monthly_income = 0
            salary_transactions = []

            for bank_account in bank_response["bankTransactions"]:
                for txn in bank_account["txns"]:
                    amount, narration, date, txn_type, mode, balance = txn

                    # Look for salary patterns (credit transactions with salary keywords)
                    if (txn_type == 1 and  # Credit transaction
                            any(keyword in narration.lower() for keyword in ['salary', 'sal', 'pay'])):
                        salary_transactions.append({
                            "amount": int(amount),
                            "date": date,
                            "narration": narration
                        })

            # Estimate monthly income (take average of salary transactions)
            if salary_transactions:
                monthly_income = sum(txn["amount"] for txn in salary_transactions) / len(salary_transactions)
            else:
                # Fallback: estimate from large credit transactions
                large_credits = []
                for bank_account in bank_response["bankTransactions"]:
                    for txn in bank_account["txns"]:
                        amount, narration, date, txn_type, mode, balance = txn
                        if txn_type == 1 and int(amount) > 50000:  # Large credit transactions
                            large_credits.append(int(amount))

                if large_credits:
                    monthly_income = max(large_credits)  # Assume largest credit is salary
                else:
                    monthly_income = 75000  # Default assumption

            result = {
                "status": "success",
                "estimated_monthly_income": int(monthly_income),
                "salary_transactions_found": len(salary_transactions)
            }
            
            # Store in session state for future reference
            tool_context.state["monthly_income"] = result
            return result
        else:
            return {"status": "error", "error_message": "Failed to fetch bank transaction data"}

    except Exception as e:
        return {"status": "error", "error_message": f"Error estimating income: {str(e)}"}


def monte_carlo_goal_simulation(
        current_age: int,
        target_age: int,
        target_amount: int,
        current_portfolio: int,
        monthly_sip: int,
        equity_percentage: float,
        tool_context: ToolContext
) -> dict:
    """Runs Monte Carlo simulation to determine goal achievement probability."""
    try:
        # Simulation parameters
        num_simulations = 5000
        years_to_goal = target_age - current_age
        months_to_goal = years_to_goal * 12

        # Market assumptions (annual returns)
        equity_mean_return = 0.12  # 12% equity returns
        equity_volatility = 0.18  # 18% volatility
        debt_mean_return = 0.07  # 7% debt returns
        debt_volatility = 0.05  # 5% volatility
        inflation_rate = 0.06  # 6% inflation

        success_count = 0
        final_amounts = []

        for _ in range(num_simulations):
            portfolio_value = current_portfolio

            for month in range(months_to_goal):
                # Add monthly SIP
                portfolio_value += monthly_sip

                # Calculate monthly returns
                equity_portion = portfolio_value * (equity_percentage / 100)
                debt_portion = portfolio_value * ((100 - equity_percentage) / 100)

                # Generate random returns
                monthly_equity_return = np.random.normal(
                    equity_mean_return / 12,
                    equity_volatility / math.sqrt(12)
                )
                monthly_debt_return = np.random.normal(
                    debt_mean_return / 12,
                    debt_volatility / math.sqrt(12)
                )

                # Apply returns
                equity_portion *= (1 + monthly_equity_return)
                debt_portion *= (1 + monthly_debt_return)

                portfolio_value = equity_portion + debt_portion

            # Adjust for inflation
            real_value = portfolio_value / ((1 + inflation_rate) ** years_to_goal)
            final_amounts.append(portfolio_value)

            if portfolio_value >= target_amount:
                success_count += 1

        # Calculate statistics
        success_probability = (success_count / num_simulations) * 100
        avg_final_amount = np.mean(final_amounts)
        median_final_amount = np.median(final_amounts)
        percentile_10 = np.percentile(final_amounts, 10)
        percentile_90 = np.percentile(final_amounts, 90)

        return {
            "status": "success",
            "success_probability": round(success_probability, 2),
            "avg_final_amount": int(avg_final_amount),
            "median_final_amount": int(median_final_amount),
            "percentile_10": int(percentile_10),
            "percentile_90": int(percentile_90),
            "target_amount": target_amount,
            "simulations_run": num_simulations,
            "years_to_goal": years_to_goal,
            "monthly_sip_used": monthly_sip,
            "equity_allocation_used": equity_percentage
        }

    except Exception as e:
        return {"status": "error", "error_message": f"Error in Monte Carlo simulation: {str(e)}"}


def recommend_sip_adjustments(
        target_amount: int,
        current_portfolio: int,
        current_monthly_sip: int,
        years_to_goal: int,
        equity_percentage: float,
        monthly_income: int,
        tool_context: ToolContext
) -> dict:
    """Recommends SIP adjustments to improve goal achievement probability."""
    try:
        # Calculate required SIP for different success probabilities
        recommendations = []

        # Target success rates to optimize for
        target_probabilities = [50, 70, 85, 95]

        for target_prob in target_probabilities:
            # Binary search for required SIP
            low_sip = 1000
            high_sip = monthly_income * 0.8  # Max 80% of income
            required_sip = current_monthly_sip

            for _ in range(20):  # Binary search iterations
                test_sip = (low_sip + high_sip) / 2

                # Quick simulation with 1000 runs for speed
                simulation_result = monte_carlo_goal_simulation(
                    current_age=30,  # Default assumption
                    target_age=30 + years_to_goal,
                    target_amount=target_amount,
                    current_portfolio=current_portfolio,
                    monthly_sip=int(test_sip),
                    equity_percentage=equity_percentage,
                    tool_context=tool_context
                )

                if simulation_result.get("status") == "success":
                    success_prob = simulation_result["success_probability"]

                    if success_prob >= target_prob:
                        high_sip = test_sip
                        required_sip = test_sip
                    else:
                        low_sip = test_sip
                else:
                    break

            sip_increase = required_sip - current_monthly_sip
            sip_increase_percentage = (sip_increase / current_monthly_sip * 100) if current_monthly_sip > 0 else 0
            affordability = "Affordable" if required_sip <= monthly_income * 0.3 else "Stretch" if required_sip <= monthly_income * 0.5 else "Challenging"

            recommendations.append({
                "target_probability": target_prob,
                "required_monthly_sip": int(required_sip),
                "sip_increase_needed": int(sip_increase),
                "sip_increase_percentage": round(sip_increase_percentage, 1),
                "affordability": affordability
            })

        return {
            "status": "success",
            "current_monthly_sip": current_monthly_sip,
            "monthly_income": monthly_income,
            "recommendations": recommendations
        }

    except Exception as e:
        return {"status": "error", "error_message": f"Error generating SIP recommendations: {str(e)}"}


def analyze_asset_allocation_impact(
        target_amount: int,
        current_portfolio: int,
        monthly_sip: int,
        years_to_goal: int,
        current_equity_percentage: float,
        tool_context: ToolContext
) -> dict:
    """Analyzes impact of different asset allocation strategies."""
    try:
        allocation_scenarios = [
            {"name": "Conservative", "equity_percentage": 30},
            {"name": "Moderate", "equity_percentage": 50},
            {"name": "Balanced", "equity_percentage": 70},
            {"name": "Aggressive", "equity_percentage": 85},
            {"name": "Very Aggressive", "equity_percentage": 95}
        ]

        results = []

        for scenario in allocation_scenarios:
            simulation = monte_carlo_goal_simulation(
                current_age=30,  # Default assumption
                target_age=30 + years_to_goal,
                target_amount=target_amount,
                current_portfolio=current_portfolio,
                monthly_sip=monthly_sip,
                equity_percentage=scenario["equity_percentage"],
                tool_context=tool_context
            )

            if simulation.get("status") == "success":
                results.append({
                    "allocation_name": scenario["name"],
                    "equity_percentage": scenario["equity_percentage"],
                    "success_probability": simulation["success_probability"],
                    "avg_final_amount": simulation["avg_final_amount"],
                    "percentile_10": simulation["percentile_10"],
                    "percentile_90": simulation["percentile_90"]
                })

        # Find optimal allocation
        best_allocation = max(results, key=lambda x: x["success_probability"]) if results else None

        return {
            "status": "success",
            "current_equity_percentage": current_equity_percentage,
            "allocation_analysis": results,
            "recommended_allocation": best_allocation,
            "current_vs_optimal": {
                "current_allocation": f"{current_equity_percentage}% Equity",
                "optimal_allocation": f"{best_allocation['equity_percentage']}% Equity" if best_allocation else "N/A",
                "probability_improvement": round(best_allocation["success_probability"] -
                                                 next((r["success_probability"] for r in results
                                                       if abs(r["equity_percentage"] - current_equity_percentage) < 5),
                                                      0), 2) if best_allocation else 0
            }
        }

    except Exception as e:
        return {"status": "error", "error_message": f"Error analyzing asset allocation: {str(e)}"}


def generate_goal_insights(
        simulation_results: dict,
        sip_recommendations: dict,
        allocation_analysis: dict,
        tool_context: ToolContext
) -> dict:
    """Generates comprehensive insights and recommendations for goal achievement."""
    try:
        insights = {
            "goal_feasibility": "",
            "key_recommendations": [],
            "risk_factors": [],
            "action_items": []
        }

        # Analyze feasibility
        success_prob = simulation_results.get("success_probability", 0)

        if success_prob >= 85:
            insights[
                "goal_feasibility"] = "Highly Achievable - Your current strategy has a high probability of success!"
        elif success_prob >= 70:
            insights["goal_feasibility"] = "Achievable with Discipline - Good probability with consistent investing."
        elif success_prob >= 50:
            insights["goal_feasibility"] = "Moderately Challenging - Requires optimization of strategy."
        else:
            insights["goal_feasibility"] = "Requires Significant Changes - Current strategy needs major adjustments."

        # Generate recommendations
        if sip_recommendations.get("status") == "success":
            affordable_recs = [r for r in sip_recommendations["recommendations"]
                               if r["affordability"] in ["Affordable", "Stretch"]]
            if affordable_recs:
                best_rec = max(affordable_recs, key=lambda x: x["target_probability"])
                insights["key_recommendations"].append(
                    f"Increase SIP to ₹{best_rec['required_monthly_sip']:,} for {best_rec['target_probability']}% success probability"
                )

        if allocation_analysis.get("status") == "success":
            improvement = allocation_analysis["current_vs_optimal"]["probability_improvement"]
            if improvement > 5:
                optimal_allocation = allocation_analysis["recommended_allocation"]["equity_percentage"]
                insights["key_recommendations"].append(
                    f"Optimize asset allocation to {optimal_allocation}% equity for {improvement:.1f}% higher success rate"
                )

        # Risk factors
        if success_prob < 70:
            insights["risk_factors"].append("Low success probability with current strategy")

        market_volatility_risk = simulation_results.get("percentile_10", 0)
        target = simulation_results.get("target_amount", 1)
        if market_volatility_risk < target * 0.7:
            insights["risk_factors"].append("High sensitivity to market downturns")

        # Action items
        insights["action_items"].append("Review and adjust SIP amount quarterly")
        insights["action_items"].append("Monitor portfolio allocation and rebalance annually")
        insights["action_items"].append("Consider increasing SIP with salary increments")

        if success_prob < 50:
            insights["action_items"].append("Consider extending timeline or reducing target amount")

        return {
            "status": "success",
            "insights": insights,
            "summary_stats": {
                "current_success_probability": f"{success_prob}%",
                "target_amount_formatted": f"₹{simulation_results.get('target_amount', 0):,}",
                "years_to_goal": simulation_results.get("years_to_goal", 0),
                "median_final_amount": f"₹{simulation_results.get('median_final_amount', 0):,}"
            }
        }

    except Exception as e:
        return {"status": "error", "error_message": f"Error generating insights: {str(e)}"}