def sign(a) -> int:
    """
    sign: returns 1 if a is positive, -1 if a is negative and 0 if a is 0
    """
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0

def lerp(a: float, b: float, t: float) -> float:
    """
    lerp: Linear intERPolation. 
        Interpolates a value from a to b based on a third value, 
        t which is a float between 0 and 1 (percentage)
        This function is mostly used for animations
    """
    return (1 - t) * a + t * b