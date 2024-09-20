def calculate_interest(principal, rate, time):
    return principal * (rate / 100) * time


print(calculate_interest(5000, .5, 12))