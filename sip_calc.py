def sip_calculator(inputs: dict) -> dict:
    """
    Calculates the future value of a Systematic Investment Plan (SIP) with regular contributions
    and a specified rate of return compounded monthly.

    Parameters:
    inputs (dict): A dictionary with the following keys:
        - 'monthly_investment' (float): The amount invested every month.
        - 'rate_of_return' (float): Expected annual rate of return (in percentage).
        - 'years' (int): Number of years the SIP is invested.

    Returns:
    dict: A dictionary with details of the SIP including the future value or an error message.
    """
    try:
        monthly_investment = float(inputs.get('monthly_investment', 0))
        rate_of_return = float(inputs.get('rate_of_return', 0)) / 100  # Convert to decimal
        years = int(inputs.get('years', 0))
        
        if monthly_investment < 0 or rate_of_return < 0 or years < 0:
            return {"error": "All input values must be non-negative."}
        
        monthly_rate = rate_of_return / 12
        total_months = years * 12
        
        if monthly_rate == 0:
            future_value = monthly_investment * total_months  # Simple sum if rate is 0
        else:
            future_value = monthly_investment * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
        
        return {
            "monthly_investment": monthly_investment,
            "rate_of_return": inputs.get('rate_of_return', 0),
            "years": years,
            "future_value": round(future_value, 2)
        }

    except ValueError:
        return {"error": "Invalid input: Ensure all inputs are numbers."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# Example usage
inputs = {
    "monthly_investment": 2000,
    "rate_of_return": 12,
    "years": 10
}
result = sip_calculator(inputs)
print(result)
