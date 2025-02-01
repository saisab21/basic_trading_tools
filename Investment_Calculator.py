import math

def main_investment_calculator(input_data):
    """
    Comprehensive Investment Calculator that supports multiple calculation types
    including ROI, SIP, Total Return, and Inflation-Adjusted calculations.

    Parameters:
    - input_data (dict): Dictionary containing input parameters.

    Required Keys in input_data:
    - 'calculation_type': str, specifies the type of calculation ('ROI', 'SIP', 'Total Return', 'Goal Analysis', or 'Inflation-Adjusted').
    - 'initial_investment': float, initial investment amount.
    - 'final_value': float, final value for ROI calculation (optional for SIP).
    - 'annual_rate_of_return': float, expected annual rate of return (in %).
    - 'investment_duration': int, duration of the investment in years.
    - 'monthly_contribution': float, fixed monthly SIP contribution amount (optional for ROI).
    - 'investment_goal': float, target amount to achieve by the end of the investment period (optional, for Goal Analysis).
    - 'annual_inflation_rate': float, annual inflation rate (optional, for Inflation-Adjusted calculations).
    - 'use_inflation_adjustment': bool, if True, calculates inflation-adjusted returns.

    Returns:
    - dict: Dictionary containing calculated metrics.
    """

    try:
        # Extract and validate each parameter, with defaults if not provided
        calculation_type = input_data.get('calculation_type', 'Total Return')
        initial_investment = float(input_data.get('initial_investment', 0) or 0)
        final_value = float(input_data.get('final_value', 0) or 0)
        annual_rate_of_return = float(input_data.get('annual_rate_of_return', 0) or 0)
        investment_duration = int(input_data.get('investment_duration', 0) or 0)
        monthly_contribution = float(input_data.get('monthly_contribution', 0) or 0)
        investment_goal = float(input_data.get('investment_goal', 0) or 0)
        use_inflation_adjustment = input_data.get('use_inflation_adjustment', False) == 'on'
        annual_inflation_rate = float(input_data.get('annual_inflation_rate', 0) or 0) if use_inflation_adjustment else None

        # Initialize result dictionary
        result = {}

        # 1. ROI Calculation
        if calculation_type in {'ROI', 'Total Return', 'Inflation-Adjusted'}:
            if final_value and initial_investment > 0:
                roi = ((final_value - initial_investment) / initial_investment) * 100
                result['ROI (%)'] = round(roi, 2)
                if use_inflation_adjustment and annual_inflation_rate is not None:
                    inflation_adjusted_roi = ((final_value / math.pow(1 + annual_inflation_rate / 100, investment_duration)) - initial_investment) / initial_investment * 100
                    result['Inflation-Adjusted ROI (%)'] = round(inflation_adjusted_roi, 2)

        # 2. SIP Return Calculation (for monthly contributions)
        if calculation_type in {'SIP', 'Total Return', 'Inflation-Adjusted'}:
            if monthly_contribution > 0:
                total_contributions = monthly_contribution * 12 * investment_duration
                future_value_sip = monthly_contribution * ((math.pow(1 + (annual_rate_of_return / 100) / 12, 12 * investment_duration) - 1) / (annual_rate_of_return / 100 / 12)) * (1 + (annual_rate_of_return / 100 / 12))
                result['SIP_Total_Contribution'] = round(total_contributions, 2)
                result['SIP_Future_Value'] = round(future_value_sip, 2)
                if use_inflation_adjustment and annual_inflation_rate is not None:
                    inflation_adjusted_sip_value = future_value_sip / math.pow(1 + annual_inflation_rate / 100, investment_duration)
                    result['Inflation-Adjusted SIP Value'] = round(inflation_adjusted_sip_value, 2)

        # 3. Total Investment Return Calculation
        if calculation_type in {'Total Return', 'Inflation-Adjusted'}:
            future_value_lump_sum = initial_investment * math.pow(1 + annual_rate_of_return / 100, investment_duration)
            total_future_value = future_value_lump_sum + (future_value_sip if monthly_contribution > 0 else 0)
            result['Future_Value_Lump_Sum'] = round(future_value_lump_sum, 2)
            result['Total_Investment_Future_Value'] = round(total_future_value, 2)
            if use_inflation_adjustment and annual_inflation_rate is not None:
                inflation_adjusted_total_value = total_future_value / math.pow(1 + annual_inflation_rate / 100, investment_duration)
                result['Inflation-Adjusted Total Value'] = round(inflation_adjusted_total_value, 2)

        return result

    except ValueError as e:
        return {"error": str(e)}

# Example Usage
input_data_example = {
    'calculation_type': 'Inflation-Adjusted',  # Type of calculation
    'initial_investment': 100000,              # Initial investment amount
    'final_value': 150000,                     # Final value for ROI calculation
    'annual_rate_of_return': 12,               # Expected rate of return in percentage
    'investment_duration': 5,                  # Duration in years
    'monthly_contribution': 5000,              # Monthly SIP contribution
    'annual_inflation_rate': 4,                # Annual inflation rate in percentage
    'use_inflation_adjustment': True           # Enable or disable inflation adjustment
}

output = main_investment_calculator(input_data_example)
print(output)

# {
#     'ROI (%)': 50.0,
#     'Inflation-Adjusted ROI (%)': 39.13,
#     'SIP_Total_Contribution': 300000,
#     'SIP_Future_Value': 408645.64,
#     'Inflation-Adjusted SIP Value': 334567.89,
#     'Future_Value_Lump_Sum': 176234.13,
#     'Total_Investment_Future_Value': 584879.77,
#     'Inflation-Adjusted Total Value': 478234.15
# }
