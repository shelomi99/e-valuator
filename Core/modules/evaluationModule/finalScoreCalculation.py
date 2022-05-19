import math


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


# function to calculate the final score
def calculate_final_score(mark_percentage, marks_allocated):
    rounded_percentage = round_up(mark_percentage, 1)
    final_mark = (rounded_percentage / 100) * float(marks_allocated)
    return rounded_percentage, round_up(final_mark, 1)
