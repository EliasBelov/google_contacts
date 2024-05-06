import time
import types

def timer_decorator(obj):
    if isinstance(obj, types.FunctionType): # если это функция
        def function_wrapper(*args, **kwargs):
            start_time = time.time()
            result = obj(*args, **kwargs)
            end_time = time.time()
            elapsed_time_seconds = int(end_time - start_time)
            elapsed_time_minutes = elapsed_time_seconds // 60
            if elapsed_time_minutes > 0:
                print(f"Функция '{obj.__name__}' заняла {elapsed_time_minutes} мин. {elapsed_time_seconds % 60} сек.")
            else:
                print(f"Функция '{obj.__name__}' заняла {elapsed_time_seconds} сек.")
            return result
        return function_wrapper
    elif isinstance(obj, type): # если это класс
        class Wrapper(obj):
            def __getattribute__(self, attr_name):
                attr_value = super().__getattribute__(attr_name)
                if callable(attr_value):
                    return timer_decorator(attr_value)
                return attr_value
        return Wrapper
