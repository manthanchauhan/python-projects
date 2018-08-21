print("enter: Numerator, denominator, number of decimal places")
dividend, divisor, decimalplaces = input().split(', ')
dividend = int(dividend)
divisor = int(divisor)
decimalplaces = int(decimalplaces)
quotient = dividend // divisor
print(quotient,end = '.')
remainder = dividend % divisor
for place in range(0, decimalplaces - 1):
    dividend = remainder * 10
    quotient = dividend // divisor
    print(quotient, end = '')
    remainder = dividend % divisor
dividend = remainder * 10
quotientTemp = dividend // divisor
remainder = dividend % divisor
dividend = remainder * 10
quotient = dividend // divisor
if (quotient > 5):
    quotientTemp += 1
print(quotientTemp)
