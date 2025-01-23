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
        {'r': 0.05, 'x': -0.2, 'y': -0.2}   # смещённый 2
    ),
    # Длина шашки
    "length": 1.0
}

# Массив толщин сгоревшего свода (для примера)
e_values = np.linspace(0, R, 200)

# Для анимации
fig, ax = plt.subplots(num="Анимация")
ax.set(xlabel="$e$, м", ylabel="$S$, м$^2$", aspect="equal")
ax.grid(True)
camera = Camera(fig)

# Расчёт площади поверхности горения
S_values = []
for e in e_values:
    S, surface = calc_burning_area(e, propellant)
    S_values.append(S)

    # Кадр для анимации
    ax.add_patch(Circle([0, 0], R, color="grey", alpha=0.4))
    xy = []
    if surface.geom_type == "MultiPolygon":
        xy.extend([g.exterior.xy for g in surface.geoms])
    else:
        xy.append(surface.exterior.xy)
    for x, y in xy:
        ax.plot(x, y, c="r")
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
