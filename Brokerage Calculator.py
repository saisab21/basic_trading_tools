def comprehensive_brokerage_calculator(input_data):
    """
    Comprehensive Calculator for Indian Stock Market Trades with selective calculations based on user input.
    
    Parameters:
    - input_data (dict): Dictionary containing user inputs.
    
    Required Keys:
    - 'broker': str, name of the broker (e.g., 'Zerodha', 'Upstox', 'Angel Broking').
    - 'transaction_type': str, type of transaction (e.g., 'equity_delivery', 'equity_intraday', 'futures', 'options').
    - 'trade_value': float, the trade value in INR.
    - 'calculations': list, contains calculation types the user wants ('brokerage', 'total_cost', 'margin', 'break_even', 'profit_loss', 'dividend_yield').

    Optional Keys:
    - 'entry_price': float, for profit/loss and break-even calculation.
    - 'exit_price': float, for profit/loss calculation.
    - 'dividend_per_share': float, for dividend yield calculation.
    - 'shares_held': int, for dividend yield and profit/loss calculation.
    - 'leverage_ratio': float, for margin calculation (optional, defaults to broker setting).
    
    Returns:
    - dict: Results of selected calculations or all calculations if no specific selection.
    """

    try:
        # Brokerage rules template for brokers, add new broker templates here
        BROKERAGE_RULES = {
            'Zerodha': {
                'equity_delivery': {'fixed': 0, 'percent': 0},
                'equity_intraday': {'fixed': 20, 'percent': 0.03},
                'futures': {'fixed': 20, 'percent': 0.03},
                'options': {'fixed': 20, 'percent': 0.03},
                'margin_ratio': {'equity_intraday': 10, 'futures': 5}  # Example leverage ratios
            },
            'Upstox': {
                'equity_delivery': {'fixed': 0, 'percent': 0},
                'equity_intraday': {'fixed': 20, 'percent': 0.05},
                'futures': {'fixed': 20, 'percent': 0.05},
                'options': {'fixed': 20, 'percent': 0.05},
                'margin_ratio': {'equity_intraday': 10, 'futures': 5}
            },
            'Angel Broking': {
                'equity_delivery': {'fixed': 0, 'percent': 0},
                'equity_intraday': {'fixed': 20, 'percent': 0.03},
                'futures': {'fixed': 20, 'percent': 0.03},
                'options': {'fixed': 20, 'percent': 0.03},
                'margin_ratio': {'equity_intraday': 10, 'futures': 5}
            },
            'Template Broker': {
                'equity_delivery': {'fixed': 0, 'percent': 0},
                'equity_intraday': {'fixed': 20, 'percent': 0.05},
                'futures': {'fixed': 20, 'percent': 0.05},
                'options': {'fixed': 20, 'percent': 0.05},
                'margin_ratio': {'equity_intraday': 5, 'futures': 3}  # Placeholder for leverage ratios
            }
        }

        # Extract and validate inputs
        broker = input_data.get('broker')
        transaction_type = input_data.get('transaction_type')
        trade_value = float(input_data.get('trade_value', 0))
        calculations = input_data.get('calculations', ['brokerage', 'total_cost', 'margin', 'break_even', 'profit_loss', 'dividend_yield'])
        
        # Optional inputs for specific calculations
        entry_price = float(input_data.get('entry_price', 0))
        exit_price = float(input_data.get('exit_price', 0))
        dividend_per_share = float(input_data.get('dividend_per_share', 0))
        shares_held = int(input_data.get('shares_held', 0))
        leverage_ratio = input_data.get('leverage_ratio', None) or BROKERAGE_RULES[broker].get('margin_ratio', {}).get(transaction_type, 0)

        # Check for invalid broker or transaction type
        if broker not in BROKERAGE_RULES:
            return {"error": "Unsupported broker. Please select a valid broker."}
        if transaction_type not in BROKERAGE_RULES[broker]:
            return {"error": "Invalid transaction type."}
        if trade_value <= 0:
            return {"error": "Trade value must be a positive number."}

        # Initialize results dictionary
        results = {"broker": broker, "transaction_type": transaction_type, "trade_value": trade_value}

        # 1. Brokerage Calculation
        if 'brokerage' in calculations:
            brokerage_data = BROKERAGE_RULES[broker][transaction_type]
            percent_brokerage = trade_value * (brokerage_data['percent'] / 100)
            brokerage = min(brokerage_data['fixed'], percent_brokerage) if brokerage_data['fixed'] > 0 else percent_brokerage
            results['brokerage'] = round(brokerage, 2)

        # 2. Total Transaction Cost Calculation
        if 'total_cost' in calculations:
            stt = trade_value * 0.001  # STT of 0.1%
            gst = (brokerage + stt) * 0.18 if 'brokerage' in results else 0  # GST on brokerage
            exchange_fees = trade_value * 0.0001  # Exchange fees
            stamp_duty = trade_value * 0.00015  # Stamp duty
            total_transaction_cost = brokerage + stt + gst + exchange_fees + stamp_duty
            results['total_transaction_cost'] = round(total_transaction_cost, 2)

        # 3. Margin Requirement Calculation
        if 'margin' in calculations and transaction_type in BROKERAGE_RULES[broker].get('margin_ratio', {}):
            margin_required = trade_value / leverage_ratio if leverage_ratio > 0 else trade_value
            results['margin_required'] = round(margin_required, 2)

        # 4. Break-Even Price Calculation
        if 'break_even' in calculations and shares_held > 0:
            break_even_price = (trade_value + total_transaction_cost) / shares_held if shares_held > 0 else 0
            results['break_even_price'] = round(break_even_price, 2)

        # 5. Intraday Profit & Loss Calculation
        if 'profit_loss' in calculations and shares_held > 0:
            profit_loss = (exit_price - entry_price) * shares_held - total_transaction_cost if shares_held > 0 else 0
            results['profit_loss'] = round(profit_loss, 2)

        # 6. Dividend Yield Calculation
        if 'dividend_yield' in calculations and trade_value > 0:
            dividend_yield = (dividend_per_share * shares_held) / trade_value * 100
            results['dividend_yield'] = round(dividend_yield, 2)

        # Final amount after brokerage if applicable
        if 'brokerage' in results and 'total_cost' in results:
            results['final_amount_after_brokerage'] = round(trade_value - total_transaction_cost, 2)

        return results

    except (ValueError, TypeError) as e:
        return {"error": f"Invalid input: {str(e)}"}

# Example usage
input_data_example = {
    'broker': 'Zerodha',
    'transaction_type': 'equity_intraday',
    'trade_value': 100000,
    'calculations': ['brokerage', 'profit_loss'],  # Specify calculations
    'entry_price': 500,
    'exit_price': 510,
    'dividend_per_share': 10,
    'shares_held': 200,
    'leverage_ratio': 5  # Optional, defaults to broker setting if not provided
}

# Test the function
output = comprehensive_brokerage_calculator(input_data_example)
print(output)


# Explanation :
# Selective Calculation:

# calculations input allows users to specify which calculations to perform.
# If no specific calculations are requested, all metrics are calculated by default.
# Flexible Output:

# Only the results for the requested calculations are included in the output, reducing clutter.
# Optional Fields: Only validate fields required for the requested calculations, ensuring minimal data validation.
# Template for Adding Brokers:

# Brokers can be added easily by copying the "Template Broker" dictionary and modifying it as needed.
# Error Handling and Validations:

# Ensures that inputs like trade value, broker, and transaction type are valid.
# Validates optional fields only when needed for a requested calculation, making the code flexible and efficient.
# Example Output
# If you specify only brokerage and profit_loss in calculations, you’ll get output








