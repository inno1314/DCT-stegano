# ------ External Libraries ------#
import cv2
import bitstring
import numpy as np
import zigzag as zz

# ---------- Source Files --------#
import image_preparation as img
import utils as stego

NUM_CHANNELS = 3


def embed_message(
    cover_image_filepath: str, stego_image_filepath: str, secret_message: str
) -> None:
    """Встраивание сообщения в изображение."""
    raw_cover_image = cv2.imread(cover_image_filepath, flags=cv2.IMREAD_COLOR)
    if raw_cover_image is None:
        print("Ошибка при чтении изображения")
        quit()

    height, width = raw_cover_image.shape[:2]
    # Корректируем размеры изображения, чтобы они были кратны 8
    # (Необходимо для работы DCT алгоритма)
    while height % 8:
        height += 1  # Строки
    while width % 8:
        width += 1  # Столбцы
    valid_dim = (width, height)
    padded_image = cv2.resize(raw_cover_image, valid_dim)
    cover_image_f32 = np.float32(padded_image)

    # Изображение переводится в цветовое пространство YCrCb (яркость и два цветовых канала)
    cover_image_YCC = img.YCC_Image(cv2.cvtColor(cover_image_f32, cv2.COLOR_BGR2YCrCb))

    # Пустой массив для хранения итогового изображения
    stego_image = np.empty_like(cover_image_f32)

    # Обработка каждого канала изображения
    for chan_index in range(NUM_CHANNELS):
        # Разбиваем на блоки 8х8 и вычисляем DCT
        dct_blocks = [cv2.dct(block) for block in cover_image_YCC.channels[chan_index]]

        # Коэффициенты DCT делятся на стандартную таблицу квантования JPEG
        dct_quants = [
            np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE))
            for item in dct_blocks
        ]

        # Коэффициенты преобразуются в зигзагообразный порядок
        # это упорядочит частоты, начиная с низких
        sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

        # === ВСТРАИВАНИЕ ДАННЫХ ===
        if chan_index == 0:  # Если идет обработка канала яркости (Luminance)
            secret_data = ""
            # Преобразуем сообщение в битовый формат
            for char in secret_message.encode("ascii"):
                secret_data += bitstring.pack("uint:8", char)

            if secret_data == "":
                print("Не удалось преобразовать сообщение в битовый формат")
                return

            # Внедряем сообщение в DCT коэффициенты
            embedded_dct_blocks = stego.embed_encoded_data_into_DCT(
                secret_data, sorted_coefficients
            )

            # Преобразуем зигзагообразный порядок обратно в двумерные блок
            desorted_coefficients = [
                zz.inverse_zigzag(block, vmax=8, hmax=8)
                for block in embedded_dct_blocks
            ]
        else:
            # Преобразуем зигзагообразный порядок обратно в двумерные блок
            desorted_coefficients = [
                zz.inverse_zigzag(block, vmax=8, hmax=8)
                for block in sorted_coefficients
            ]

        # Деквантование (умножение на таблицу квантования)
        dct_dequants = [
            np.multiply(data, img.JPEG_STD_LUM_QUANT_TABLE)
            for data in desorted_coefficients
        ]

        # Обратное DCT, чтобы восстановить блоки изображения
        idct_blocks = [cv2.idct(block) for block in dct_dequants]

        # Обработанные блоки собираются обратно в изображение
        stego_image[:, :, chan_index] = np.asarray(
            img.stitch_8x8_blocks_back_together(cover_image_YCC.width, idct_blocks)
        )

    # Изображение переводится обратно в цветовое пространство BGR (RGB)
    stego_image_BGR = cv2.cvtColor(stego_image, cv2.COLOR_YCR_CB2BGR)

    # Значения пикселей ограничиваются диапазоном [0, 255]
    final_stego_image = np.uint8(np.clip(stego_image_BGR, 0, 255))

    # Итоговое изображение с сообщением сохраняется в файл STEG_IMAGE_FILEPATH
    cv2.imwrite(stego_image_filepath, final_stego_image)
