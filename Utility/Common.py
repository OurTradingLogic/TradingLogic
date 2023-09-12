import numpy

def InRange(a, b, c):
    result = False
    if a >= c >= b:
        result = True
    return result

def PercentageBy(a, b):
    if a == b:
        return 100.0
    try:
        return (abs(a - b) / b) * 100.0
    except ZeroDivisionError:
        return 0
    
def PercentageBy_Solid(a, b):
    if a == b:
        return 100.0
    try:
        return ((a - b) / b) * 100.0
    except ZeroDivisionError:
        return 0
    
def FindNDifference(a, b):
    if a == b:
        return 0.0
    
    percent = PercentageBy(a, b)
    return (percent/100)

def FindDifferencePercentage(a, b):
    percent = PercentageBy(a, b)
    return abs(percent-100)

def Average(lst):
    # average function
    avg = numpy.average(lst)
    return(avg)