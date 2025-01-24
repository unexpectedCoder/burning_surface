# ПРИМЕР РАБОТЫ С ФУНКЦИЕЙ
# Все размеры и физ. величины - в единицах СИ


import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from matplotlib.patches import Circle
from shapely import Point

from burning_surface import calc_burning_area


# Внешний радиус заряда (постоянный, нет внешнего горения)
R = 0.5
# Описание геометрии заряда
# (можно сделать это как-угодно, здесь словарь для примера)
propellant = {
    # Основное поперечное сечение - круг
    "cross-section": Point(0, 0).buffer(R),
    # То же, но с чуть большим радиусом, чтобы избежать
    # влияние конечной точности float
    "float-cross-section": Point(0, 0).buffer(R + 1e-5),
    # Цилиндрические каналы в заряде:
    # могут располагаться произвольным образом 
    # и иметь любой радиус (возможны проблемы,
    # если эти размеры будут какими-то "неразумными")
    "holes": (
        {'r': 0.1, 'x': 0.0, 'y': 0.0},     # центральный
        {'r': 0.05, 'x': 0.2, 'y': 0.2},    # смещённый 1
        {'r': 0.05, 'x': -0.2, 'y': -0.2},  # смещённый 2
        {'r': 0.02, 'x': -0.2, 'y': 0.2},   # смещённый 3
        {'r': 0.01, 'x': 0.25, 'y': -0.18}  # смещённый 4
    ),
    # Длина шашки
    "length": 1.0
}


# Для анимации и итогового графика S(e)
fig, (ax1, ax2) = plt.subplots(num="Анимация", ncols=2, figsize=(8, 5))
ax1.set(xlabel="$x$, м", ylabel="$y$, м", aspect="equal")
ax2.set(xlabel="$e$, м", ylabel="$S$, м$^2$")
ax2.grid()
camera = Camera(fig)

# Массив толщин сгоревшего свода (для примера)
e_values = np.linspace(0, R, 200)
S_values = []
for i, e in enumerate(e_values, start=1):
    # Расчёт площади поверхности горения
    S, surface = calc_burning_area(e, propellant)
    S_values.append(S)

    # Кадр для анимации
    ax1.add_patch(Circle([0, 0], R, color="grey", alpha=0.4))
    xy = []
    if surface.geom_type == "MultiPolygon":
        xy.extend([g.exterior.xy for g in surface.geoms])
    elif surface.geom_type == "Polygon":
        xy.append(surface.exterior.xy)
    else:
        raise ValueError("ошибка с типом surface")
    for x, y in xy:
        ax1.plot(x, y, c="r")
        ax2.plot(e_values[:i], S_values, c="b")
    camera.snap()

# Создание анимации
ani = camera.animate()
ani.save(f"{fig.get_label()}.gif", dpi=120)
# График S(e)
fig, ax = plt.subplots(num="Зависимость S(e)")
ax.plot(e_values, S_values)
ax.set(xlabel="$e$, м", ylabel="$S$, м$^2$")
ax.grid(True)
fig.savefig(f"{fig.get_label()}.png", dpi=300)

plt.show()
