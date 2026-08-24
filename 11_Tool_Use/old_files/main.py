def greeting():
    print("Hi there")


def calculate_pi(digits=5):
    """
    Calculate pi to a specified number of decimal digits using the Machin formula.
    Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    
    Args:
        digits: Number of decimal places to calculate (default: 5)
    
    Returns:
        float: Approximation of pi to the specified digits
    """
    from decimal import Decimal, getcontext
    
    # Set precision higher than needed to ensure accuracy
    getcontext().prec = digits + 10
    
    def arctan(x, num_terms=100):
        """Calculate arctan using Taylor series expansion."""
        x = Decimal(x)
        power = x
        result = power
        for n in range(1, num_terms):
            power *= -x * x
            result += power / (2 * n + 1)
        return result
    
    # Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    pi = 4 * (4 * arctan(Decimal(1) / Decimal(5), 100) - arctan(Decimal(1) / Decimal(239), 100))
    
    # Round to specified digits
    return round(float(pi), digits)