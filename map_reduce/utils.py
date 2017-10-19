"""Модуль со вспомогательными функциями"""
import os


def is_number(value):
    try:
        float(value)
        return True
    except TypeError:
        return False


def comparator(value1, value2, reverse=False, case_sensitive=True):
    """ Сравнивает значения value1, value2.
    Возвращает 0, если значения равны.
    Возвращает 1, если value1 идет позже, чем value2
    Возвращает -1, если value1 идет раньше, чем value2
    """
    if type(value1) != type(value2):
        raise ValueError('It is impossible to compare different types: "{0}" and {1}'
                         .format(type(value1), type(value2)))
    if not isinstance(value1, int) and not isinstance(value1, str):
        raise ValueError('I don\'t know how to compare "{0}"'.format(type(value1)))
    if (value1, str) and isinstance(value2, str):
        if not case_sensitive:
            value1, value2 = value1.lower(), value2.lower()
    if value1 == value2:
        return 0
    result = 1 if value1 > value2 else -1
    if reverse:
        result *= -1
    return result


def get_next_data_piece(file, size_of_piece, separator):
    """ Возвращает кусок данных из открытого на чтение файла file, размера 
    минимум size_of_piece, пока не встретит separator или EOF"""
    if not isinstance(size_of_piece, int):
        raise TypeError('"size_of_piece" must be an int, but it is {0}:{1}'
                        .format(type(size_of_piece), size_of_piece))
    if not isinstance(separator, str):
        raise TypeError('"separator" must be an str, but it is {0}:{1}'
                        .format(type(separator), separator))
    try:
        result = file.read(size_of_piece)
        if result.endswith(separator):
            result = result[:len(result) - len(separator)]
        else:
            current = file.read(1)
            while current != '' and current != separator:
                result += current
                current = file.read(1)
        return result
    except AttributeError:
        raise AttributeError("Attribute 'file' is not readable")


def check_directory_path(directory):
    if not isinstance(directory, str):
        raise TypeError("Name of directory where lies piece must be a string")
    if not os.path.exists(directory):
        raise FileNotFoundError("Directory '{0}' is not exists".format(directory))
    if not os.path.isdir(directory):
        raise NotADirectoryError("Expected that '{}' is directory".format(directory))
    return True


def check_file_path(path):
    if not isinstance(path, str):
        print(path)
        raise TypeError("Path must be a string")
    if not os.path.exists(path):
        raise FileNotFoundError("File '{0}' does not exist".format(path))
    return True
