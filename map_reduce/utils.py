"""Модуль со вспомогательными функциями"""
import cProfile
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
        raise TypeError('"Size of one piece must be an integer but {0}:{1}'.format(type(size_of_piece), size_of_piece))
    if not isinstance(separator, str):
        raise TypeError('Separator must be a string, but {0}:{1}'.format(type(separator), separator))
    try:
        result = file.read(size_of_piece)
        if result.endswith(separator):
            result = result[:-len(separator)]
        else:
            current = file.read(1)
            while current != '' and current != separator:
                result += current
                current = file.read(1)
        return result
    except AttributeError:
        raise AttributeError("'file' attribute must have a read() method")


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
        raise TypeError("Path to file must be a string")
    if not os.path.exists(path):
        raise FileNotFoundError("File '{0}' does not exist.".format(path))
    return True

def determine_size_of_one_piece():
    try:
        import psutil
        return psutil.virtual_memory().free // 10
    except ImportError:
        return 2 * 1024 * 1024 * 1024 // 10

def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result
    return wrapper

