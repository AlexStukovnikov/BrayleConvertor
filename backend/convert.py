from music21 import converter
import csv

def convert(target_file_path, output_file_path):
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


    # Таблица соответствия символов Брайля и .brf
    with open('braille_to_brf.csv') as braille_to_pdf_file:
        braille_to_brf = dict(list(csv.reader(braille_to_pdf_file))[1:])


    # Загрузка MusicXML файла
    score = converter.parse(target_file_path)  # Укажите путь к вашему файлу
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
                print(element.notes)
                chord_symbols = [note_to_braille.get(n.nameWithOctave, '?') for n in element.notes]
                braille_notes.append("".join(chord_symbols))  # Объединяем символы нот аккорда
                print(chord_symbols)
            elif element.isRest:
                # Паузы можно обозначать отдельным символом, например, '⠿'
                braille_notes.append('⠿')

    # Конвертация файла .brf с Брайлем в ASCII
    with open(output_file_path, "w", encoding="utf-8") as output_file_path:
        ascii_line = "".join([braille_to_brf.get(i, '?') for i in braille_notes])
        output_file_path.write(ascii_line + "\n")

if __name__ == 'main':
    target_file_path = "Dichterliebe01.musicxml"
    output_file_path = "output_ascii.brf"
    convert(target_file_path, output_file_path)