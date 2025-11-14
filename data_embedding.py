# ------ External Libraries ------#
from typing import List
import bitstring
from bitstring.bitstream import BitStream
import numpy as np
from numpy.typing import NDArray


def extract_encoded_data_from_DCT(
    dct_blocks: List[NDArray[np.float64]],
) -> BitStream | None:
    """Эта функция извлекает закодированные данные из блоков DCT-коэффициентов"""
    extracted_data = ""  # Пустая строка для записи извлеченных битов
    for current_dct_block in dct_blocks:
        # Пропускается 1-ый коэффициент, т.к. он содержит информацию об интенсивности блока
        for coeff_index in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[coeff_index])
            if curr_coeff > 1:  # Если коэффициент больше 1:
                # Берем его младший бит (& 0x01) и добавляем в extracted_data
                extracted_data += bitstring.pack(
                    "uint:1", np.uint8(current_dct_block[coeff_index]) & 0x01
                )
    if extracted_data == "":
        return None
    return extracted_data


def embed_encoded_data_into_DCT(
    encoded_bits: BitStream, dct_blocks: List[NDArray[np.float64]]
) -> List:
    """Эта функция встраивает закодированные данные в блоки DCT-коэффициентов"""
    data_complete = False  # Флаг для отслеживания завершения встраивания данных
    encoded_bits.pos = 0
    # Кодируем длину данных (в 32 бита)
    encoded_data_len = bitstring.pack("uint:32", len(encoded_bits))
    converted_blocks = []

    for current_dct_block in dct_blocks:  # Для каждого блока DCT-коэффициентов:
        for coeff_index in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[coeff_index])
            if curr_coeff > 1:
                # Преобразуем коэффициент в 8-битное целое число
                curr_coeff = np.uint8(current_dct_block[coeff_index])

                # Если данные полностью встроены: выходим из цикла
                if encoded_bits.pos == (len(encoded_bits) - 1):
                    data_complete = True
                    break

                # pack_coeff — текущий коэффициент DCT в виде 8-битного числа
                # pack_coeff[-1] — младший бит коэффициента
                pack_coeff = bitstring.pack("uint:8", curr_coeff)
                if encoded_data_len.pos <= (len(encoded_data_len) - 1):
                    # Сначала записываем длину данных (в 32 бита)
                    pack_coeff[-1] = encoded_data_len.read(1)
                else:
                    # Если длина записана — начинаем записывать сообщение
                    pack_coeff[-1] = encoded_bits.read(1)

                # Записываем обновленный коэффициент обратно в блок
                current_dct_block[coeff_index] = np.float32(pack_coeff.read("uint:8"))

        converted_blocks.append(current_dct_block)

    if not (data_complete):
        raise ValueError("Не удалось встроить сообщение полностью")

    return converted_blocks
