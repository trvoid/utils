################################################################################
# Get an axis range for given values.                                          #
################################################################################

import sys

################################################################################
# Functions                                                                    #
################################################################################

def get_leading_digits(value, leading_digit_count = 1):
    if value == 0:
        return 0, 0
        
    d = value
    p = 0
    
    lb = pow(10, leading_digit_count - 1)
    ub = pow(10, leading_digit_count)
    
    if d >= lb:
        while True:
            if d < ub:
                break
            p += 1
            d = d / 10
    else:
        while True:
            if d >= lb:
                break
            p -= 1
            d = d * 10
    
    return int(d), p
    
def get_floor(value, leading_digit_count = 1):
    d, p = get_leading_digits(value, leading_digit_count)
    _value = d * pow(10, p)
    return _value, p
    
def get_ceil(value, leading_digit_count = 1):
    d, p = get_leading_digits(value, leading_digit_count)
    _value = d * pow(10, p)
    if _value != value:
        _value += pow(10, p)
    return _value, p
    
def get_axis_range(values, leading_digit_count = 1):
    max_value = max(values)
    min_value = min(values)
    
    range_max, p = get_ceil(max_value, leading_digit_count)
    resolution = pow(10, p)
    
    if range_max == max_value:
        range_max += resolution
    
    # To avoid a side-effect while dealing with floating numbers
    # ,for example, 0.19999999999999937 is returned instead of 0.2
    range_max_reduced = range_max / resolution
    range_min_reduced = range_max_reduced - 1
    min_value_reduced = min_value / resolution
    
    while True:
        if range_min_reduced < min_value_reduced:
            break
        range_min_reduced -= 1
    
    range_max = range_max_reduced * resolution
    range_min = range_min_reduced * resolution
    
    return range_min, range_max
    
def print_usage(script_name):
    print(f'Usage: python {script_name} <min_value> <max_value> <leading_digit_count>')
    print(f'        - min_value: non-negative float number')
    print(f'        - max_value: non-negative float number (max_value >= min_value)')
    print(f'        - leading_digit_count: non-negative integer number')

def main(min_value, max_value, leading_digit_count):
    values = [min_value, max_value]
    range_min, range_max = get_axis_range(values, leading_digit_count)

    print(f'[{min_value}, {max_value}] ==> axis_range: {range_min} ~ {range_max}')
    
################################################################################
# Configuration                                                                #
################################################################################

################################################################################
# Main                                                                         #
################################################################################

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_usage(sys.argv[0])
        sys.exit(-1)

    min_value = float(sys.argv[1])
    max_value = float(sys.argv[2])
    leading_digit_count = int(sys.argv[3])

    if min_value < 0 or min_value > max_value or leading_digit_count < 0:
        print_usage(sys.argv[0])
        sys.exit(-1)
        
    main(min_value, max_value, leading_digit_count)
