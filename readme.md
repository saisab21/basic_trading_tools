# README

## Overview
This project implements a SIP (Systematic Investment Plan) calculator that takes dictionary-based input and returns dictionary-based output. The exact look of this page should resemble the reference image already updated on Jira.

## Implementation Details
- The code is lightweight and can run entirely on the frontend.
- The function `sip_calculator` accepts a dictionary containing:
  - `monthly_investment` (float): Monthly investment amount.
  - `rate_of_return` (float): Annual return rate (in percentage).
  - `years` (int): Investment duration in years.
- The function returns a dictionary with the computed `future_value`.

## Integration Notes
- The provided example usage in the code should be commented out before embedding.
- Ensure the frontend properly handles dictionary inputs and outputs.

## Usage Example (Commented Out in Code)
```python
# Example usage (Comment this out in production)
inputs = {
    "monthly_investment": 2000,
    "rate_of_return": 12,
    "years": 10
}
result = sip_calculator(inputs)
print(result)  # Expected output: {'monthly_investment': ..., 'rate_of_return': ..., 'years': ..., 'future_value': ...}
