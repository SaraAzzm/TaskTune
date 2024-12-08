from flask import redirect, session
from datetime import datetime
from functools import wraps


def deadline(date):
    """Formats a date"""
    deadline = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%y %H:%M:%S")
    return f"{deadline[:-3]}"


def date_comparison(date):
    """Read dates for comparison"""
    formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return formatted_date


def calculate_percentages(total, start, end, statistics, statistic_list):
    """Return statistics and their corresponding percentage"""
    if total == 0:
        for i in range(start, end):
            statistics[i]["percentage"] = 0.0
            statistics[i]["statistic"] = statistic_list[i]
    else:
        for i in range(start, end):
            statistics[i]["percentage"] = round((statistics[i]["value"] / total) * 100, 1)
            statistics[i]["statistic"] = statistic_list[i]


def get_eps_level(eps, EPS_indicators):
    """Return EPS level"""
    if eps > 0.2:
        return "High", EPS_indicators[0]
    elif eps < -0.2:
        return "Low", EPS_indicators[2]
    else:
        return "Medium", EPS_indicators[1]


def get_completion_value(percentage):
    """Return task completion level"""
    if percentage > 70:
        return "High"
    elif 40 < percentage <= 70:
        return "Medium"
    else:
        return "Low"


def get_correlation_indicator(eps_level, completion_level, correlation_indicators):
    """Return EPS and task completion correlation indicator"""
    if eps_level == "High":
        return correlation_indicators[0] if completion_level in ["High", "Medium"] else correlation_indicators[1]
    elif eps_level == "Medium":
        return correlation_indicators[2] if completion_level in ["High", "Medium"] else correlation_indicators[3]
    else:
        return correlation_indicators[4] if completion_level in ["High", "Medium"] else correlation_indicators[5]


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
