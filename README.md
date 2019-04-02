# numerical-analysis

## HW1

### Задание 1

 1. Выбрать полином нечетной степени
 2. Локализовать корни
 3. С помощью метода бисекций, итеративного метода и метода Ньютона вычислить первый найденный корень с заданой точностью

### Задание 2

Уравнение `x = r * x * (1 - x)`, `r > 0`. Корни вычисляются с помощью метода простых итераций.
Найти `r1`, `r2` и `r3`, для которых верно: 
 1. Если `r < r1`, то `xn -> x1` 
 2. Если `r1 < r < r2`, то `xn -> x2` монотонно
 3. Если `r2 < r < r3`, то `xn -> x2` колебательно
 4. Если `r > r3`, то `rn` расходится
Также, построить графики сходимости для разных `r` и постротить траекторию сходимости метода простых итераций

### Задание 3

Для уравнения `z ^ 3 - 1 = 0` на плоскости `[-2, 2] * [-2, 2]` для каждой точки цветом обозначить, к какому из корней она сходится 
