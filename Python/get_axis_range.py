################################################################################
# Get an axis range for given values.                                          #
#                                                                              #
# Example:                                                                     #
#     For a value range (-41 ~ 35), axis range can be                          #
#         (-50 ~ 40) if leading digit count is 1, or                           #
#         (-42 ~ 36) if leading digit count is 2.                              #
################################################################################

import sys

################################################################################
# Functions                                                                    #
################################################################################

# Arguments:
#     value - float.
#     leading_digit_count - positive integer.
# Returns:
#     sign, leading digits, resolution
def get_leading_digits(value, leading_digit_count = 1):
    if leading_digit_count < 1:
        raise RuntimeError(f'leading_digit_count({leading_digit_count}) is less than 1.')
        
    s = 1 if value >= 0 else -1
    d = abs(value)
    p = 0

    if d > 0:
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
    
    return s, int(d), pow(10, p)
    
def get_floor(value, leading_digit_count = 1):
    s, d, r = get_leading_digits(value, leading_digit_count)
    _value = s * d * r
    if value < 0 and _value != value:
        _value -= r
    return _value, r
    
def get_ceil(value, leading_digit_count = 1):
    s, d, r = get_leading_digits(value, leading_digit_count)
    _value = s * d * r
    if value > 0 and _value != value:
        _value += r
    return _value, r
    
def get_axis_range(values, leading_digit_count = 1):
    max_value = max(values)
    min_value = min(values)
    
    if abs(max_value) >= abs(min_value):
        range_max, resolution = get_ceil(max_value, leading_digit_count)
        
        # To avoid a side-effect while dealing with floating numbers
        # ,for example, 0.19999999999999937 is returned instead of 0.2
        range_max_reduced = range_max / resolution
        range_min_reduced = range_max_reduced - 1
        min_value_reduced = min_value / resolution
        
        while True:
            if range_min_reduced <= min_value_reduced:
                break
            range_min_reduced -= 1
        
        range_max = range_max_reduced * resolution
        range_min = range_min_reduced * resolution
    else:
        range_min, resolution = get_floor(min_value, leading_digit_count)
        
        # To avoid a side-effect while dealing with floating numbers
        # ,for example, 0.19999999999999937 is returned instead of 0.2
        range_min_reduced = range_min / resolution
        range_max_reduced = range_min_reduced + 1
        max_value_reduced = max_value / resolution
        
        while True:
            if range_max_reduced >= max_value_reduced:
                break
            range_max_reduced += 1
        
        range_max = range_max_reduced * resolution
        range_min = range_min_reduced * resolution
        
    return range_min, range_max, resolution
    
def print_usage(script_name):
    print(f'Usage: python {script_name} <min_value> <max_value> <leading_digit_count>')
    print(f'        - min_value: float number')
    print(f'        - max_value: float number (max_value >= min_value)')
    print(f'        - leading_digit_count: positive integer number')

def main(min_value, max_value, leading_digit_count):
    values = [min_value, max_value]
    range_min, range_max, resolution = get_axis_range(values, leading_digit_count)
    
    print(f'value range: {min_value} ~ {max_value} ==> axis range: {range_min} ~ {range_max}, resolution: {resolution}')
    
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

    if min_value > max_value or leading_digit_count < 1:
        print_usage(sys.argv[0])
        sys.exit(-1)
        
    main(min_value, max_value, leading_digit_count)
