def lerp2(b, start, end):
    """ linear interpolation of 2 vectors. """
    return (1 - b) * start + b * end

def fade(t):
    """ fades a value, simple as that really. """
    return ((6*t - 15) * t + 10) * t**3