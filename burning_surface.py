from math import pi
from shapely import Point, unary_union


def calc_burning_area(e: float, propellant: dict):
    """Рассчитать площадь поверхности горения по
    толщине сгоревшего свода `e` и геометрии заряда `propellant`.

    Returns:
        Площадь и поверхность горения.
    """
    # Выгорание внутренних каналов
    inner_holes = []
    for hole in propellant["holes"]:
        inner_hole = Point(hole['x'], hole['y']).buffer(hole['r'] + e)
        inner_holes.append(
            inner_hole.intersection(propellant["float-cross-section"])
        )
        # Использование float-cross-section выше продиктовано тем,
        # что точное пересечение окружностей компьютер посчитать не может
        # ввиду конечной точности типа float. Поэтому внешнюю окружность
        # чуток увеличиваем - на результате это не сказывается
    
    # Расчёт длины фронта горения в поперечном сечении
    surface = unary_union(inner_holes)
    holes_boundary = surface.boundary
    propel_boundary = propellant["cross-section"].boundary
    extra_boundary = propel_boundary.intersection(surface)
    perimeter = holes_boundary.length - extra_boundary.length

    # Площадь поверхности горения внутренних каналов
    S = perimeter * propellant["length"]
    nf = propellant["faces"]
    if nf == 0:
        return S, surface
    if propellant["length"] < 1e-6:
        return 0, surface
    # + площадь горения торцев
    S_faces = nf*(pi*propellant["R"]**2 - surface.area)
    # с изменением общей длины заряда
    propellant["length"] -= nf * e
    return S + S_faces, surface
