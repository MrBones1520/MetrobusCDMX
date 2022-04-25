
def get_coord(points: str) -> tuple:
    return tuple(map(float, points.split(',')))


def group_by(iterat, func, k_attr):
    lines = {}
    for it in iterat:
        attr_val = getattr(it, k_attr)
        if attr_val not in lines:
            lines[attr_val] = [func(it)]
        else:
            lines[attr_val] += [func(it)]
    return lines

