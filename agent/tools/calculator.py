# Parameter keys for calculator tool
OPERATOR_1 = "operator_1"
OPERATOR_2 = "operator_2"
OPERAND = "operand"

def calculate(args: dict) -> float:
    """
    Perform calculation based on arguments dictionary containing operand and operators.
    
    Args:
        args (dict): Dictionary containing:
            - operand: The operation type (+, -, *, /, %)
            - operator_1: First number
            - operator_2: Second number
    
    Returns:
        float: Result of the calculation or error message
    """
    try:
        # Extract values from dictionary with validation
        if OPERAND not in args:
            raise ValueError("Missing required field: " + OPERAND)
        if OPERATOR_1 not in args:
            raise ValueError("Missing required field: " + OPERATOR_1)
        if OPERATOR_2 not in args:
            raise ValueError("Missing required field: " + OPERATOR_2)
        operand = args[OPERAND]
        operator_1 = float(args[OPERATOR_1])
        operator_2 = float(args[OPERATOR_2])

        # Define operations
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: round(x / y, 2) if y != 0 else float('inf'),
            '%': lambda x, y: round((x / 100) * y, 2)
        }

        # Validate operand
        if operand not in operations:
            raise ValueError(f"Invalid operand: {operand}")

        # Perform calculation
        result = operations[operand](operator_1, operator_2)
        return result

    except (ValueError) as e:
        return f"Invalid values: {str(e)}"
    except Exception as e:
        return f"Calculation error: {str(e)}"
    
def generate_response(calculated_result) -> str:
    """
    Generate a user-friendly response based on the calculation result.
    
    Args:
        calculated_result (float or str): The result of the calculation or an error message.
    
    Returns:
        str: A formatted response string.
    """
    return f"The result of the calculation is: {calculated_result}"