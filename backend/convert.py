from music21 import converter
from typing import Callable
from functools import wraps
import csv
import os
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)
def convert(target_file_path, output_file_path):

    def _error_handler(*exceptions: Exception, title="Ошибка", desc=None, level=logging.WARNING):
        def _handler(f: Callable):
            @wraps(f)
            def _wrapper(*args, **kwargs):
                try:
                    f(*args, **kwargs)
                except exceptions as e:
                    e.add_note(title)
                    e.add_note(desc)
                    e.add_note(str(level))
                    logging.log(level, e)
                    raise
            return _wrapper
        return _handler


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
    @_error_handler(FileNotFoundError, title='Ошибка компонента', desc="Компонент не найден, проверьте целостность файлов или переустановите программу", level=logging.ERROR)
    def _fill_braille_to_brf():
        with open(os.path.join(os.path.dirname(__file__), 'braille_to_brf.csv')) as _:
            nonlocal braille_to_brf
            braille_to_brf = dict(list(csv.reader(_))[1:])
    _fill_braille_to_brf()

    score = []
    @_error_handler(converter.ConverterException,title='Ошибка поиска файла', desc='Файл не найден')
    @_error_handler(converter.ConverterFileException,title='Ошибка конвертации', desc='Содержимое файла не может быть сконвертировано')
    def _parse_input_file():
        nonlocal score 
        score = converter.parse(target_file_path)
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
    @_error_handler(FileExistsError, title='Ошибка записи', desc='Файл уже существует')
    def _write_output():
        with open(output_file_path, "x", encoding="utf-8") as output_file:
            output = " ".join([braille_to_brf.get(i, '?') for i in braille_notes])
            output_file.write(output + "\n")
    _write_output()

if __name__ == '__main__':
    FILE_ROOT = os.path.dirname(__file__)
    target_file_path = os.path.join(FILE_ROOT, "We_Will_Rock_you.mxl")
    output_file_path = os.path.join(FILE_ROOT, "We_Will_Rock_you.brf")
    convert(target_file_path, output_file_path)