import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from google.adk.agents import Agent

# Mock Database - Replace with actual Firestore in production
MOCK_DATABASE = {
    "balance_forecasts": {
        "forecast_user_abc_20250726_060000": {
            "id": "forecast_user_abc_20250726_060000",
            "user_id": "user_abc",
            "forecast_generated_at": "2025-07-26T06:00:00Z",
            "current_balance": 15750.00,
            "model_used": "Prophet",
            "model_accuracy": 0.87,
            "forecast_horizon_days": 90,
            "daily_predictions": [
                {
                    "date": "2025-07-27",
                    "day_offset": 1,
                    "predicted_balance": 15900.00,
                    "confidence_lower": 15700.00,
                    "confidence_upper": 16100.00,
                    "expected_income": 0.00,
                    "expected_expenses": -150.00,
                    "net_flow": -150.00
                },
                {
                    "date": "2025-07-28",
                    "day_offset": 2,
                    "predicted_balance": 15850.00,
                    "confidence_lower": 15500.00,
                    "confidence_upper": 16200.00,
                    "expected_income": 0.00,
                    "expected_expenses": -200.00,
                    "net_flow": -200.00
                },
                {
                    "date": "2025-09-15",
                    "day_offset": 51,
                    "predicted_balance": 3200.00,  # Below safety buffer
                    "confidence_lower": 2800.00,
                    "confidence_upper": 3600.00,
                    "expected_income": 0.00,
                    "expected_expenses": -300.00,
                    "net_flow": -300.00
                },
                {
                    "date": "2025-10-01",
                    "day_offset": 67,
                    "predicted_balance": 78200.00,  # Salary credit
                    "confidence_lower": 77800.00,
                    "confidence_upper": 78600.00,
                    "expected_income": 75000.00,
                    "expected_expenses": -250.00,
                    "net_flow": 74750.00
                }
            ],
            "summary_stats": {
                "min_balance": {
                    "amount": 3200.00,
                    "date": "2025-09-15",
                    "days_from_now": 51
                },
                "max_balance": {
                    "amount": 78200.00,
                    "date": "2025-10-01",
                    "days_from_now": 67
                },
                "avg_daily_burn": -185.50,
                "volatile_periods": [
                    {
                        "start_date": "2025-09-10",
                        "end_date": "2025-09-20",
                        "reason": "High spending + no income"
                    }
                ]
            },
            "risk_analysis": {
                "days_below_buffer": 12,
                "probability_negative": 0.15,
                "worst_case_balance": 1800.00,
                "buffer_breach_dates": ["2025-09-15", "2025-09-16", "2025-09-17"]
            }
        }
    },

    "alerts": {
        "alert_user_abc_20250726_060015": {
            "id": "alert_user_abc_20250726_060015",
            "user_id": "user_abc",
            "alert_type": "balance_warning",
            "severity": "high",
            "forecast_id": "forecast_user_abc_20250726_060000",
            "trigger_details": {
                "breach_date": "2025-09-15",
                "predicted_balance": 3200.00,
                "safety_buffer": 5000.00,
                "deficit": 1800.00,
                "days_until_breach": 51,
                "confidence": 0.78
            },
            "context": {
                "recent_spending_trend": "increased_by_15%",
                "upcoming_income": {
                    "next_salary_date": "2025-08-01",
                    "amount": 75000.00,
                    "days_away": 6
                },
                "major_upcoming_expenses": [
                    {
                        "date": "2025-08-15",
                        "amount": 12000.00,
                        "description": "Credit card bill"
                    }
                ]
            },
            "ai_generated_summary": "Your account balance is predicted to drop below ₹5,000 on September 15th, reaching ₹3,200. This creates a ₹1,800 deficit from your safety buffer.",
            "suggested_actions": [
                {
                    "action": "reduce_discretionary_spending",
                    "description": "Cut non-essential expenses by ₹200/day for next 10 days",
                    "impact": "saves_2000_over_10_days",
                    "effort": "medium"
                },
                {
                    "action": "delay_large_purchase",
                    "description": "Postpone your ₹3,000 entertainment budget to next month",
                    "impact": "immediate_3000_saving",
                    "effort": "low"
                },
                {
                    "action": "increase_income",
                    "description": "Consider freelance work to earn extra ₹2,000",
                    "impact": "adds_2000_buffer",
                    "effort": "high"
                }
            ],
            "status": "pending",
            "created_at": "2025-07-26T06:00:15Z",
            "expires_at": "2025-07-26T18:00:00Z"
        }
    },

    "user_settings": {
        "user_abc": {
            "user_id": "user_abc",
            "safety_buffer": 5000.00,
            "currency": "INR",
            "alert_preferences": {
                "email": True,
                "push": True,
                "websocket": True,
                "advance_days": 7
            },
            "forecast_settings": {
                "model_preference": "Prophet",
                "forecast_horizon": 90,
                "update_frequency": "6_hours"
            }
        }
    }
}


# Tool 1: Get Current Financial Health
def get_current_financial_health(user_id: str = "user_abc") -> Dict[str, Any]:
    """
    Retrieves the current financial health overview including current balance,
    90-day forecast, and risk metrics for the specified user.

    Args:
        user_id: The user identifier (defaults to user_abc for demo)

    Returns:
        Dictionary containing current financial health data
    """
    try:
        # Get latest forecast
        forecasts = MOCK_DATABASE.get("balance_forecasts", {})
        latest_forecast = None

        for forecast_id, forecast_data in forecasts.items():
            if forecast_data.get("user_id") == user_id:
                latest_forecast = forecast_data
                break

        if not latest_forecast:
            return {"error": f"No forecast data found for user {user_id}"}

        # Get user settings
        user_settings = MOCK_DATABASE.get("user_settings", {}).get(user_id, {})
        safety_buffer = user_settings.get("safety_buffer", 5000.00)

        # Calculate health score
        current_balance = latest_forecast.get("current_balance", 0)
        min_balance = latest_forecast.get("summary_stats", {}).get("min_balance", {}).get("amount", 0)

        health_score = min(100, max(0, (current_balance / (safety_buffer * 2)) * 100))

        return {
            "user_id": user_id,
            "current_balance": current_balance,
            "safety_buffer": safety_buffer,
            "health_score": round(health_score, 1),
            "forecast_horizon": latest_forecast.get("forecast_horizon_days"),
            "model_accuracy": latest_forecast.get("model_accuracy"),
            "min_predicted_balance": min_balance,
            "min_balance_date": latest_forecast.get("summary_stats", {}).get("min_balance", {}).get("date"),
            "days_until_min": latest_forecast.get("summary_stats", {}).get("min_balance", {}).get("days_from_now"),
            "avg_daily_burn": latest_forecast.get("summary_stats", {}).get("avg_daily_burn"),
            "risk_analysis": latest_forecast.get("risk_analysis", {}),
            "currency": user_settings.get("currency", "INR"),
            "last_updated": latest_forecast.get("forecast_generated_at")
        }

    except Exception as e:
        return {"error": f"Error retrieving financial health: {str(e)}"}


# Tool 2: Check for Financial Alerts
def check_financial_alerts(user_id: str = "user_abc", severity_filter: str = "all") -> Dict[str, Any]:
    """
    Checks for any pending financial alerts for the user, with optional severity filtering.

    Args:
        user_id: The user identifier (defaults to user_abc for demo)
        severity_filter: Filter by severity ('all', 'high', 'critical', 'medium')

    Returns:
        Dictionary containing active alerts and their details
    """
    try:
        alerts = MOCK_DATABASE.get("alerts", {})
        user_alerts = []

        for alert_id, alert_data in alerts.items():
            if (alert_data.get("user_id") == user_id and
                    alert_data.get("status") == "pending"):

                # Apply severity filter
                if severity_filter != "all" and alert_data.get("severity") != severity_filter:
                    continue

                user_alerts.append(alert_data)

        # Sort by severity and date
        severity_order = {"critical": 3, "high": 2, "medium": 1, "low": 0}
        user_alerts.sort(key=lambda x: (
            severity_order.get(x.get("severity", "low"), 0),
            x.get("created_at", "")
        ), reverse=True)

        return {
            "user_id": user_id,
            "total_alerts": len(user_alerts),
            "severity_filter": severity_filter,
            "alerts": user_alerts,
            "summary": {
                "critical": len([a for a in user_alerts if a.get("severity") == "critical"]),
                "high": len([a for a in user_alerts if a.get("severity") == "high"]),
                "medium": len([a for a in user_alerts if a.get("severity") == "medium"]),
                "low": len([a for a in user_alerts if a.get("severity") == "low"])
            }
        }

    except Exception as e:
        return {"error": f"Error retrieving alerts: {str(e)}"}


# Tool 3: Find Risk Periods
def find_risk_periods(user_id: str = "user_abc", balance_threshold: Optional[float] = None) -> Dict[str, Any]:
    """
    Identifies specific time periods when the user's balance is predicted to be below
    their safety buffer or a custom threshold.

    Args:
        user_id: The user identifier (defaults to user_abc for demo)
        balance_threshold: Custom threshold to check against (uses safety_buffer if None)

    Returns:
        Dictionary containing risk periods and their details
    """
    try:
        # Get latest forecast
        forecasts = MOCK_DATABASE.get("balance_forecasts", {})
        latest_forecast = None

        for forecast_id, forecast_data in forecasts.items():
            if forecast_data.get("user_id") == user_id:
                latest_forecast = forecast_data
                break

        if not latest_forecast:
            return {"error": f"No forecast data found for user {user_id}"}

        # Get threshold
        if balance_threshold is None:
            user_settings = MOCK_DATABASE.get("user_settings", {}).get(user_id, {})
            balance_threshold = user_settings.get("safety_buffer", 5000.00)

        # Find risk periods
        daily_predictions = latest_forecast.get("daily_predictions", [])
        risk_periods = []
        current_period = None

        for prediction in daily_predictions:
            predicted_balance = prediction.get("predicted_balance", 0)

            if predicted_balance < balance_threshold:
                if current_period is None:
                    # Start new risk period
                    current_period = {
                        "start_date": prediction.get("date"),
                        "start_balance": predicted_balance,
                        "min_balance": predicted_balance,
                        "min_balance_date": prediction.get("date"),
                        "days": 1,
                        "total_deficit": balance_threshold - predicted_balance
                    }
                else:
                    # Extend current period
                    current_period["days"] += 1
                    current_period["total_deficit"] += (balance_threshold - predicted_balance)
                    if predicted_balance < current_period["min_balance"]:
                        current_period["min_balance"] = predicted_balance
                        current_period["min_balance_date"] = prediction.get("date")
            else:
                if current_period is not None:
                    # End current period
                    current_period["end_date"] = daily_predictions[daily_predictions.index(prediction) - 1].get("date")
                    current_period["avg_daily_deficit"] = current_period["total_deficit"] / current_period["days"]
                    risk_periods.append(current_period)
                    current_period = None

        # Handle case where risk period extends to end of forecast
        if current_period is not None:
            current_period["end_date"] = daily_predictions[-1].get("date")
            current_period["avg_daily_deficit"] = current_period["total_deficit"] / current_period["days"]
            risk_periods.append(current_period)

        return {
            "user_id": user_id,
            "balance_threshold": balance_threshold,
            "total_risk_periods": len(risk_periods),
            "total_risk_days": sum(period["days"] for period in risk_periods),
            "risk_periods": risk_periods,
            "overall_risk_level": "high" if len(risk_periods) > 2 else "medium" if len(risk_periods) > 0 else "low",
            "next_risk_date": risk_periods[0]["start_date"] if risk_periods else None
        }

    except Exception as e:
        return {"error": f"Error finding risk periods: {str(e)}"}


# Tool 4: Get Action Recommendations
def get_action_recommendations(user_id: str = "user_abc", focus_area: str = "all") -> Dict[str, Any]:
    """
    Retrieves AI-generated action recommendations to improve the user's financial situation.

    Args:
        user_id: The user identifier (defaults to user_abc for demo)
        focus_area: Filter recommendations by focus ('all', 'spending', 'income', 'savings')

    Returns:
        Dictionary containing personalized action recommendations
    """
    try:
        # Get pending alerts with suggestions
        alerts = MOCK_DATABASE.get("alerts", {})
        recommendations = []

        for alert_id, alert_data in alerts.items():
            if (alert_data.get("user_id") == user_id and
                    alert_data.get("status") == "pending"):

                suggested_actions = alert_data.get("suggested_actions", [])
                for action in suggested_actions:
                    # Apply focus filter
                    action_type = action.get("action", "")
                    if focus_area != "all":
                        if focus_area == "spending" and "spending" not in action_type:
                            continue
                        elif focus_area == "income" and "income" not in action_type:
                            continue
                        elif focus_area == "savings" and "saving" not in action_type:
                            continue

                    recommendations.append({
                        **action,
                        "alert_id": alert_id,
                        "alert_type": alert_data.get("alert_type"),
                        "priority": alert_data.get("severity")
                    })

        # Sort by priority and effort
        priority_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        effort_order = {"low": 3, "medium": 2, "high": 1}

        recommendations.sort(key=lambda x: (
            priority_order.get(x.get("priority", "low"), 1),
            effort_order.get(x.get("effort", "high"), 1)
        ), reverse=True)

        # Add some general recommendations based on financial health
        health_data = get_current_financial_health(user_id)
        health_score = health_data.get("health_score", 50)

        general_recommendations = []
        if health_score < 30:
            general_recommendations.append({
                "action": "emergency_budget",
                "description": "Create an emergency budget to reduce expenses by 30%",
                "impact": "significant_expense_reduction",
                "effort": "high",
                "category": "spending"
            })
        elif health_score < 60:
            general_recommendations.append({
                "action": "spending_review",
                "description": "Review and categorize all expenses from last month",
                "impact": "better_spending_awareness",
                "effort": "medium",
                "category": "spending"
            })

        if health_score > 70:
            general_recommendations.append({
                "action": "investment_opportunity",
                "description": "Consider investing surplus funds in liquid mutual funds",
                "impact": "improved_returns",
                "effort": "low",
                "category": "savings"
            })

        return {
            "user_id": user_id,
            "focus_area": focus_area,
            "health_score": health_score,
            "total_recommendations": len(recommendations) + len(general_recommendations),
            "urgent_actions": [r for r in recommendations if r.get("priority") in ["critical", "high"]],
            "quick_wins": [r for r in recommendations + general_recommendations if r.get("effort") == "low"],
            "all_recommendations": recommendations + general_recommendations,
            "categories": {
                "spending": len(
                    [r for r in recommendations + general_recommendations if "spending" in r.get("action", "")]),
                "income": len(
                    [r for r in recommendations + general_recommendations if "income" in r.get("action", "")]),
                "savings": len([r for r in recommendations + general_recommendations if r.get("category") == "savings"])
            }
        }

    except Exception as e:
        return {"error": f"Error retrieving recommendations: {str(e)}"}

