# Зигзагообразное сканирование матрицы
# Аргументом является двумерная матрица любого размера,
# не обязательно квадратная.
# Функция возвращает массив размером 1 на (m*n),
# где m и n - размеры входной матрицы,
# состоящий из элементов, отсканированных зигзагообразным методом.

import numpy as np


def zigzag(input):
    h = 0
    v = 0

    vmin = 0
    hmin = 0

    vmax = input.shape[0]
    hmax = input.shape[1]

    i = 0

    output = np.zeros((vmax * hmax))

    while (v < vmax) and (h < hmax):
        if ((h + v) % 2) == 0:  # идем вверх
            if v == vmin:
                output[i] = input[v, h]  # если мы дошли до первой строки

                if h == hmax:
                    v = v + 1
                else:
                    h = h + 1

                i = i + 1

            elif (h == hmax - 1) and (v < vmax):  # если мы дошли до последего столбца
                output[i] = input[v, h]
                v = v + 1
                i = i + 1

            elif (v > vmin) and (h < hmax - 1):  # все остальные случаи
                output[i] = input[v, h]
                v = v - 1
                h = h + 1
                i = i + 1

        else:  # идем вниз
            if (v == vmax - 1) and (h <= hmax - 1):  # если мы дошли до последей строки
                output[i] = input[v, h]
                h = h + 1
                i = i + 1

            elif h == hmin:  # если мы дошли до первого столбца
                output[i] = input[v, h]

                if v == vmax - 1:
                    h = h + 1
                else:
                    v = v + 1

                i = i + 1

            elif (v < vmax - 1) and (h > hmin):  # все остальные случаи
                output[i] = input[v, h]
                v = v + 1
                h = h - 1
                i = i + 1

        if (v == vmax - 1) and (h == hmax - 1):  # нижний правый элемент
            output[i] = input[v, h]
            break

    return output


# Обратное зигзагообразное сканирование матрицы
# Аргументами являются: массив размером 1 на m*n,
# где m и n - размеры выходной матрицы по вертикали и горизонтали.
# Функция возвращает двумерную матрицу определенных размеров,
# состоящую из элементов входного массива, собранных зигзагообразным методом.


def inverse_zigzag(input, vmax, hmax):
    # инициализация переменных
    h = 0
    v = 0

    vmin = 0
    hmin = 0

    output = np.zeros((vmax, hmax))

    i = 0

    while (v < vmax) and (h < hmax):
        if ((h + v) % 2) == 0:  # идем вверх
            if v == vmin:  # Если мы дошли до первой строки
                output[v, h] = input[i]

                if h == hmax:
                    v = v + 1
                else:
                    h = h + 1

                i = i + 1

            elif (h == hmax - 1) and (v < vmax):  # если мы дошли до последего столбца
                output[v, h] = input[i]
                v = v + 1
                i = i + 1

            elif (v > vmin) and (h < hmax - 1):  # остальные случаи
                output[v, h] = input[i]
                v = v - 1
                h = h + 1
                i = i + 1

        else:  # идем вниз
            if (v == vmax - 1) and (h <= hmax - 1):  # если мы дошли до последей строки
                output[v, h] = input[i]
                h = h + 1
                i = i + 1

            elif h == hmin:  # если мы дошли до первого столбца
                output[v, h] = input[i]
                if v == vmax - 1:
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1

            elif (v < vmax - 1) and (h > hmin):  # все остальные случаи
                output[v, h] = input[i]
                v = v + 1
                h = h - 1
                i = i + 1

        if (v == vmax - 1) and (h == hmax - 1):  # нижний правый элемент
            output[v, h] = input[i]
            break

    return output


# Примеры использования функций
if __name__ == "__main__":
    # Пример 1: Зигзагообразное сканирование
    matrix = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    print("Исходная матрица:")
    print(matrix)

    zigzag_result = zigzag(matrix)
    print("Результат зигзагообразного сканирования:")
    print(zigzag_result)

    # Пример 2: Обратное зигзагообразное сканирование
    reconstructed_matrix = inverse_zigzag(zigzag_result, 4, 4)
    print("Восстановленная матрица:")
    print(reconstructed_matrix)
