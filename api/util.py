import os

basedir = os.path.abspath(os.path.dirname(__file__))


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


class Configuration(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
