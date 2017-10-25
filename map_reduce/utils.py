"""Модуль со вспомогательными функциями"""
import os


def is_number(value):
    """ Проверяет, является ли value целым числом или вещественным. 

    Args:
        value (object): значение, которое нужно проверить.
         
    Returns:
        True, если value int или float, иначе False.
    """
    try:
        float(value)
        return True
    except Exception:
        return False


def get_next_data_piece(file, size_of_piece, separator):
    """ Возвращает кусок данных из открытого на чтение файла file, размера 
    минимум size_of_piece, пока не встретит separator или EOF.

    Args:
        file(readable object): файл, открытый на чтение. В общем случае, объект, для которого определен метод read().
        size_of_piece(int): примерное количество байт(нижняя граница), отводимое для одного куска файла. 
        separator (str): разделитель между значениями.

    Returns:    
        Строку str - следующий фрагмент файла.

    Raises:
        TypeError: если size_of_piece не является целым числом.
        TypeError: если separator не является строкой.
        AttributeError: если file не имеет атрибут read().
        """
    if not isinstance(size_of_piece, int):
        raise TypeError('"size_of_piece" должно быть целым числом, но она {0}:{1}'
                        .format(type(size_of_piece), size_of_piece))
    if not isinstance(separator, str):
        raise TypeError('"separator" должен быть строкой str, но он {0}:{1}'
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
        raise AttributeError("Атрибут 'file' не имеет метода read()")


def check_directory_path(directory):
    """ Проверяет, что папка directory существует. 
        
    Returns:
        Если папка существует, возвращается True.
        
    Raises:
        TypeError: если directory не является строкой.
        FileNotFoundError: если пути directory не существует.
        NotADirectoryError: если directory - не папка, а файл.

    """
    if not isinstance(directory, str):
        raise TypeError("Имя папки должно быть строкой, но оно {0}.".format(type(directory)))
    if not os.path.exists(directory):
        raise FileNotFoundError("Такой директории не существует: {0}.".format(directory))
    if not os.path.isdir(directory):
        raise NotADirectoryError("Ожидалось, что '{}' директория, но это файл.".format(directory))
    return True


def check_file_path(path):
    """ Проверяет, что файл по пути path существует.
    
    Args:
        path: путь до файла.

    Raises:
        TypeError: если path не является строкой.
        FileNotFoundError: если файла по пути path не существует.

    Returns:
        True, если файл существует.
    """
    if not isinstance(path, str):
        raise TypeError("Путь до файла должен быть строкой")
    if not os.path.exists(path):
        raise FileNotFoundError("Файла '{0}' не существует".format(path))
    return True
