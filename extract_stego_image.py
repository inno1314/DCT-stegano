# ------ External Libraries ------#
import cv2
import struct
import numpy as np
import zigzag as zz

# ---------- Source Files --------#
import data_embedding as stego
import image_preparation as img


def read_embedded_message(stego_image_filepath: str):
    """Чтение сообщения из изображения."""
    stego_image = cv2.imread(stego_image_filepath, flags=cv2.IMREAD_COLOR)
    if stego_image is None:
        print("Ошибка при чтении изображения")
        quit()

    stego_image_f32 = np.float32(stego_image)
    # Преобразуем изображение из цветового пространства BGR (RGB) в YCrCb
    stego_image_YCC = img.YCC_Image(cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb))

    # Прямое косинусное преобразование (DCT)
    dct_blocks = [
        cv2.dct(block) for block in stego_image_YCC.channels[0]
    ]  # Используем только канал яркости, так как он содержит основную информацию

    # Квантование, деление коэффициентов DCT на стандартную таблицу квантования
    dct_quants = [
        np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE)) for item in dct_blocks
    ]

    # Коэффициенты DCT сортируются в порядке увеличения частоты
    sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

    # === ИЗВЛЕЧЕНИЕ ДАННЫХ ===
    recovered_data = stego.extract_encoded_data_from_DCT(sorted_coefficients)
    if recovered_data is None:
        return "Не удалось извлечь сообщение"
    recovered_data.pos = 0  # Устанавливаем указатель чтения в начало данных

    # Определение длины сообщения:
    # Читаем первые 32 бита (4 байта), которые содержат длину скрытого сообщения
    data_len = int(recovered_data.read("uint:32") / 8)

    # Извлечение сообщения из DCT коэффициентов
    extracted_data = bytes()
    for _ in range(data_len):  # Цикл извлекает сообщение байт за байтом
        # struct.pack() преобразует каждый байт в формат,
        # пригодный для объединения в итоговое сообщение
        extracted_data += struct.pack(">B", recovered_data.read("uint:8"))

    return extracted_data.decode("ascii")
