def annualized_return_calculator(inputs):
    """
    Calculates the annualized return on an investment.

    Parameters:
    inputs (dict): A dictionary with the following keys:
        - 'initial_investment' (float): Initial amount invested.
        - 'final_value' (float): Final value of the investment.
        - 'years' (int): Number of years the investment was held.

    Returns:
    dict: A dictionary with the calculated annualized return or an error message.
    """
    try:
        initial_investment = float(inputs.get('initial_investment', 0))
        final_value = float(inputs.get('final_value', 0))
        years = int(inputs.get('years', 0))

        if initial_investment <= 0 or final_value < 0 or years <= 0:
            return {"error": "Initial investment, final value, and years must be positive."}

        annualized_return = ((final_value / initial_investment) ** (1 / years) - 1) * 100

        return {
            "initial_investment": initial_investment,
            "final_value": final_value,
            "years": years,
            "annualized_return": round(annualized_return, 2)
        }

    except ValueError:
        return {"error": "Invalid input: Ensure all inputs are numbers."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# Example usage
inputs = {
    "initial_investment": 10000,
    "final_value": 15000,
    "years": 3
}

result = annualized_return_calculator(inputs)
print(result)
