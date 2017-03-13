def box(x1, y1, w1, h1,
        x2, y2, w2, h2):
    if x1 + w1 <= x2:
        return False
    if x1 >= x2 + w2:
        return False
    if y1 + h1 <= y2:
        return False
    if y1 >= y2 + h2:
        return False
    return True
