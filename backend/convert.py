from music21 import converter
from typing import Callable
from functools import wraps
import csv
import os
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=1)
def convert(target_file_path, output_file_path):
    def file_not_found_handler(f: Callable):
        @wraps(f)
        def wrapper():
            try:
                f()
            except FileNotFoundError or converter.ConverterException as e:
                logging.exception(e)
                raise
        return wrapper
    
    def file_exists_handler(f: Callable):
        @wraps(f)
        def wrapper():
            try:
                f()
            except FileExistsError as e:
                logging.exception(e)
                raise
        return wrapper
    
    # Генерация таблицы соответствий
    note_to_braille = {}
    # Символы для натуральных нот, диезов и бемолей
    natural_base = {'C': '⠙', 'D': '⠑', 'E': '⠋', 'F': '⠛', 'G': '⠓', 'A': '⠊', 'B': '⠌'}
    sharp_prefix = '⠘'  # Диез
    flat_prefix = '⠰'  # Бемоль

    # Генерация соответствий для октав от 0 до 8
    for octave in range(9):  # От 0 до 8 включительно
        for note, braille_symbol in natural_base.items():
            note_to_braille[f"{note}{octave}"] = braille_symbol # Натуральные ноты
            note_to_braille[f"{note}#{octave}"] = sharp_prefix + braille_symbol # Диезы
            note_to_braille[f"{note}♭{octave}"] = flat_prefix + braille_symbol # Бемоли

    braille_to_brf = []
    # Таблица соответствия символов Брайля и .brf
    @file_not_found_handler
    def _fill_brf():
        with open(os.path.join(os.path.dirname(__file__), 'braille_to_brf.csv')) as _:
            nonlocal braille_to_brf
            braille_to_brf = dict(list(csv.reader(_))[1:])
    _fill_brf()

    score = []
    @file_not_found_handler
    def _parse_input_file():
        nonlocal score 
        score = converter.parse(target_file_path)  # Укажите путь к вашему файлу
    _parse_input_file()
    
    # Переменная для хранения нот в Брайле
    braille_notes = []
    # Извлечение нот и преобразование в Брайль
    for part in score.parts:
        for element in part.flatten().notesAndRests:
            if element.isNote:
                # Преобразование одиночной ноты
                pitch = element.nameWithOctave  # Например, 'C4'
                braille_symbol = note_to_braille.get(pitch, '?')  # '?' если нота не найдена
                braille_notes.append(braille_symbol)
            elif element.isChord:
                # Преобразование аккорда
                chord_symbols = [note_to_braille.get(n.nameWithOctave, '?') for n in element.notes]
                braille_notes.append("".join(chord_symbols))  # Объединяем символы нот аккорда
            elif element.isRest:
                # Паузы можно обозначать отдельным символом, например, '⠿'
                braille_notes.append('⠿')

    # Конвертация файла .brf с Брайлем в ASCII
    @file_exists_handler
    def _fill_brf():
        with open(output_file_path, "x", encoding="utf-8") as output_file:
            output = " ".join([braille_to_brf.get(i, '?') for i in braille_notes])
            output_file.write(output + "\n")
    _fill_brf()

if __name__ == '__main__':
    FILE_ROOT = os.path.dirname(__file__)
    target_file_path = os.path.join(FILE_ROOT, "We_Will_Rock_you.mxl")
    output_file_path = os.path.join(FILE_ROOT, "We_Will_Rock_you.brf")
    convert(target_file_path, output_file_path)