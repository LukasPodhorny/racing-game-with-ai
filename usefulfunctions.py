def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):

    # Calculate slopes of the lines
    m1 = (y2 - y1) / (x2 - x1) if x2 != x1 else None
    m2 = (y4 - y3) / (4 - x3) if x4 != x3 else None
    
    # If both lines are vertical (parallel)
    if m1 is None and m2 is None:
        return None
    
    # If one of the lines is vertical
    if m1 is None:
        x = x1
        y = m2 * (x - x3) + y3
    elif m2 is None:
        x = x3
        y = m1 * (x - x1) + y1
    else:
        # If lines are not parallel, find the intersection point
        if m1 == m2:
            return None  # Lines are parallel, no intersection
        x = ((m1 * x1 - m2 * x3) + y3 - y1) / (m1 - m2)
        y = m1 * (x - x1) + y1
    
    return x, y