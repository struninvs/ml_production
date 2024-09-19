"""
Данный модуль - это небольшая надстройка над стандартным модулем logging для:
1) Кодирования всех записей журнала логирования в JSON-формат определенной структуры;
2) Связывания логов с помощью correlation_id;
3) Создания контекста, с помощью которого вывод сторонних модулей можно перевести в требуемый формат;
   Это необходимо в случае, если логирование проходит по ELK-пайплайну и к формату ведения журнала предъявляются
   определенные требования (наличие обязательных полей, формат данных и др.).
4) Перехвата warning независимо от того, в каком фрагменте кода они возникли.

ВАЖНО: 
Концепция связывания логов работает для синхронного выполнения кода, а также выполнения кода в многопоточном или
мультипроцессорном режиме. Для асинхронного выполнения кода correlation_id необходимо передавать вручную каждый раз
при создании записи в журнале логирования. Минусом такого способа задания correlation_id является то, что мы не сможем 
связывать логи, которые генерируют сторонние модули.

TODO:
1) correlation_id_dict сделать переменной класса JSONLogFormatter и управлять им через класс JSONLogger.
   Эту задачу можно также реализовать через переопределение метода logging.Logger.makeRecord в классе JSONLogger.
   Пример:
   https://stackoverflow.com/questions/59176101/extract-the-extra-fields-in-logging-call-in-log-formatter
"""
import functools
import sys
import threading
import time
import uuid
import datetime
import json
import logging
import contextlib

from pydantic import BaseModel
from typing import Union, Dict, Any, Callable

global handler, formatter, correlation_id_dict
correlation_id_dict: Dict[str, str] = {}

class JsonLogSchema(BaseModel):
    """Форма записи в JSON формате для ведения логов.

    Перечень обязательных полей составлен с учетом последующей выгрузки логов для анализа из ES в DWH.
    Поле extra - это непараметризованное поле для хранения разных данных, необходимых для анализа (например, оценки ML-модели).
    Поле debug_info нужно для отладки.
    """

    # обязательные поля:
    correlation_id: str # это поле автоматически заполняется, если ранее была вызвана ф-ия bind_correlation_id()
    written_at: str
    msg: str
    level: str
    id: str
    parent_id: str
    user_id: str
    item_id: str
    merchant_id : str
    content_type: str
    
    # дополнительные поля:
    extra: Union[Dict[str, Any], None] = None

    # поля для отладки:
    debug_info: Union[Dict[str, Any], None] = None

class JSONLogFormatter(logging.Formatter):
    
    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        log_object: dict = self._format_log_object(record, *args, **kwargs)
        return json.dumps(log_object, ensure_ascii = False)
    
    def _format_log_object(self, record: logging.LogRecord, *args, **kwargs) -> dict:
        """Перевод записи объекта журнала в json формат с необходимым перечнем полей.

        Объект record нам передает класс Logger модуля logging в виде словаря, где уже стандартные и extra поля, 
        которые в методах класса Logger (log, info, debug и т.п.) передаются через одноименный параметр. Наша
        задача отделить extra поля от predefined_keys, который формируется в теле метода и зависит в том числе
        от набора полей в JsonLogSchema.

        Такое решение можно реализовать также на уровне класса Logger: 
        https://stackoverflow.com/questions/59176101/extract-the-extra-fields-in-logging-call-in-log-root_formatter
        однако логика нам немного не подходит, поэтому реализовали по-своему.

        correlation_id может быть присвоен записи в двух случаях:
        - если до создания записи в журнале была вызвана bind_correlation_id();
        - если в при создании записи через параметр extra был передан словарь с ключем correlation_id.
        Во всех остальных случаях correlation_id останется пустым.
        """

        global correlation_id_dict

        debug_info_keys = ["threadName", "name", "module", "lineno", "exc_info", "exc_text", "stack_info"]        
        predefined_keys = ["name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module",  
                           "lineno", "exc_info", "exc_text", "stack_info", "funcName", "created", "msecs", "relativeCreated", 
                           "thread", "threadName", "processName", "process"] + list(JsonLogSchema.__dict__.keys())
        extra_keys = [key for key in record.__dict__.keys() if key not in predefined_keys and record.__dict__[key] is not None]
        thread = str(record.threadName)
        if thread in correlation_id_dict.keys():
            correlation_id = correlation_id_dict[thread]
        elif hasattr(record, "correlation_id"):
            correlation_id = str(record.__dict__["correlation_id"])
        else:
            correlation_id = ""

        # Инициализация тела журнала
        json_log_fields = JsonLogSchema(
            correlation_id = correlation_id,
            msg = str(record.getMessage()),
            level = str(record.levelname),            
            id = str(record.__dict__["id"]) if hasattr(record, "id") else "",
            parent_id = str(record.__dict__["parent_id"]) if hasattr(record, "parent_id") else "",
            user_id = str(record.__dict__["user_id"]) if hasattr(record, "user_id") else "",
            item_id = str(record.__dict__["item_id"]) if hasattr(record, "item_id") else "",
            merchant_id = str(record.__dict__["merchant_id"]) if hasattr(record, "merchant_id") else "",
            content_type = str(record.__dict__["content_type"]) if hasattr(record, "content_type") else "",
            written_at = str(datetime.datetime.fromtimestamp(record.created).astimezone().replace().isoformat()),
            extra = {key: str(record.__dict__[key]) if record.__dict__[key] is not None else None for key in extra_keys},
            debug_info = {key: str(record.__dict__[key]) if record.__dict__[key] is not None else None for key in debug_info_keys}
            )
        
        # Преобразование Pydantic объекта в словарь
        json_log_object = json_log_fields.__dict__

        return json_log_object

handler = logging.StreamHandler(sys.stdout)
formatter = JSONLogFormatter()
handler.setFormatter(formatter)

class JSONLogger(logging.Logger):
    """Класс JSONLogger предназначен для ведения журнала в виде JSON-объектов.

    Основная логика и операции форматирования происходят в классе JSONLogFormatter.    
    """
    def __init__(self, name, logging_level: int = logging.DEBUG, context_logging_level: int = logging.DEBUG):
        # инициируем класс и привяжем к нему обработчик JSON:
        super().__init__(name, logging_level)
        global handler, formatter
        self.addHandler(handler)
        # настроим ведение журнала для записей, которые генерирует модуль warnings:
        logging.captureWarnings(True)
        logging.getLogger('py.warnings').addHandler(handler)
        # настроим поведение контекстного менеджера для обработки стандартного вывода:
        self.context_logging_level = context_logging_level
        self._redirector = contextlib.redirect_stdout(self)  # type: ignore

    @classmethod
    def bind_correlation_id(cls) -> None:
        """Позволяет потокобезопасно связать несколько запросов между собой с помощью uuid.
        
        В контексте связывания логов сервисов, построенных на FastAPI, предполагается, что
        функция bind_correlation_id() будет вызываться в Middleware-функции: 
        https://fastapi.tiangolo.com/tutorial/middleware/ 
        
        Для безопасного использования correlation_id должна использоваться функция flush_correlation_id(),
        которая должна вызываться в обработчике ручки.

        При асинхронном выполнении программы correlation_id не будет нести своей смысловой нагрузки.
        """
        global correlation_id_dict

        thread_name = threading.current_thread().name
        correlation_id_dict[thread_name] = str(uuid.uuid1())
        return None

    @classmethod
    def flush_correlation_id(cls) -> None:
        """Позволяет удалить correlation_id.

        Это безопасный вариант использования correlation_id, но не всегда является обязательным использование
        этой функции, если использование одного и того же correlation_id повторно не подразумевается кодом.
        """
        thread_name = threading.current_thread().name
        if thread_name in correlation_id_dict.keys():
            del correlation_id_dict[thread_name]
        return None

    def write(self, msg):
        """Метод write необходим для правильной работы класса при использования с контекстным менеджером из contextlib.

        Позволяет применять форматированное логирование для обычных выводов через stdout.

        Пример:
        logger = JSONLogger("main")

        with logger:
            print("Test json logger stdout hook!")
        """
        if msg and not msg.isspace():
            self.log(msg = msg, level = self.context_logging_level)

    def flush(self):
        """Метод flush необходим для правильной работы класса при использования с контекстным менеджером из contextlib.

        Позволяет применять форматированное логирование для обычных выводов через stdout.
        
        Пример:
        logger = JSONLogger("main")

        with logger:
            print("Test json logger stdout hook!")
        """
        sys.stdout.flush()

    def __enter__(self):
        """Метод __enter__ необходим для правильной работы класса при использования с контекстным менеджером из contextlib.

        Позволяет применять форматированное логирование для обычных выводов через stdout.
        
        Пример:
        logger = JSONLogger("main")

        with logger:
            print("Test json logger stdout hook!")
        """
        self._redirector.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Метод __exit__ необходим для правильной работы класса при использования с контекстным менеджером из contextlib.

        Позволяет применять форматированное логирование для обычных выводов через stdout.
        
        Пример:
        logger = JSONLogger("main")

        with logger:
            print("Test json logger stdout hook!")
        """
        self._redirector.__exit__(exc_type, exc_value, traceback)

    def timeit(self, logging_level: int = logging.DEBUG)-> Callable[..., Callable[..., Any]]:
        """Декоратор для измерения длительности выполнения функций
        
        Пример:
        logger = JSONLogger("main")

        @logger.timeit()
        def division_by_zero(a: int):
            return 1/(a - 1)
        """
        def decorator(func)-> Callable[..., Any]:
            @functools.wraps(func)
            def wrapper(*args, **kwargs)-> Any:
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                self.log(msg = f"func {func.__name__} executed in {round(execution_time, 2)} seconds", level = logging_level)
                return result
            return wrapper
        return decorator


if __name__ == "__main__":
    """
    Здесь приведен небольшой пример как можно пользоваться модулем.
    """
    logger = JSONLogger(__name__)

    @logger.timeit()
    def division_by_zero(a: int):
        return 1/(a - 1)
    
    def hiden_traceback_division_by_zero(a: int):
        b = a - 1
        return division_by_zero(b)

    logger.bind_correlation_id() # вызываем в месте, где начинаются связанные логи

    d1 = {
        "This" : "is",
        "e_x_t_r_a" : "fields"
    }
    
    logger.info("Logger init!!!", extra = d1)

    try:
        division_by_zero(1)
    except Exception:
        logger.exception("Выполнение функции division_by_zero завершилось с ошибкой!")

    division_by_zero(2)

    with logger:
        print("Test json logger stdout hook!")

    logger.flush_correlation_id()
    try:
        hiden_traceback_division_by_zero(2)
    except Exception as ex:
        logger.exception(msg = "Processed error")