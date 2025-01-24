from shapely.geometry import Point
from shapely.ops import unary_union


def calc_burning_area(e, propellant):
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
    perimeter = holes_boundary.length - extra_boundary.length#
    
    # Площадь поверхности горения
    return perimeter * propellant["length"], surface
