import csv
from crewai.tools import tool

@tool("Read Merchant Data")
def read_merchant_data(file_path: str) -> str:
    """
    Reads merchant performance data from a CSV file and returns it as a 
    formatted string. Use this tool when you need to access merchant order 
    frequency, SLA breach rates, and courier type data.
    """
    try:
        merchants = []
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                merchants.append(row)
        
        if not merchants:
            return "No merchant data found in file."
        
        formatted = "MERCHANT PERFORMANCE DATA:\n\n"
        for m in merchants:
            formatted += f"""Merchant: {m['merchant_name']} (ID: {m['merchant_id']})
  Zone: {m['zone']}
  Orders (Week 1/2/3): {m['orders_week1']} / {m['orders_week2']} / {m['orders_week3']}
  Avg Delivery Time: {m['avg_delivery_time']} mins
  SLA Breach Rate: {float(m['sla_breach_rate'])*100:.1f}%
  Courier Type: {m['courier_type']}\n\n"""
        
        return formatted
    
    except FileNotFoundError:
        return f"Error: File not found at {file_path}. Check the path and try again."
    except Exception as e:
        return f"Error reading merchant data: {str(e)}"


@tool("Calculate Severity Score")
def calculate_severity_score(
    orders_week1: int, 
    orders_week2: int, 
    orders_week3: int, 
    sla_breach_rate: float
) -> str:
    """
    Calculates a severity score for a merchant based on order trend and SLA 
    breach rate. Returns a score from 0-100 and a severity label. 
    Use this tool after identifying a merchant with declining orders to 
    quantify how urgent the intervention is.
    Input sla_breach_rate as a decimal e.g. 0.31 not 31.
    """
    try:
        # Order trend score — how steep is the decline?
        avg_early = (orders_week1 + orders_week2) / 2
        if avg_early == 0:
            trend_score = 50
        else:
            decline_pct = (avg_early - orders_week3) / avg_early
            trend_score = min(decline_pct * 100, 50)

        # SLA score — how bad is the breach rate?
        sla_score = min(sla_breach_rate * 100, 50)

        # Combined severity
        severity = trend_score + sla_score

        if severity >= 60:
            label = "CRITICAL"
        elif severity >= 35:
            label = "HIGH"
        elif severity >= 15:
            label = "MEDIUM"
        else:
            label = "LOW"

        return f"Severity Score: {severity:.1f}/100 — {label}"
    
    except Exception as e:
        return f"Error calculating severity: {str(e)}"