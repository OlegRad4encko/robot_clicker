import logging
import ast
import sys
import time
from functions_ import write, press, click, doubleClick, mouseDown, mouseUp, moveTo, pause, make_area_taps

logging.basicConfig(
    filename='error_log.log',  # Имя файла для записи логов
    level=logging.ERROR,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)


def start_profile(profile_name, queue):
    custom_profile(profile_name, queue)


def custom_profile(profile, queue):
    time.sleep(0.1)
    queue.put({"work": 1})
    time.sleep(0.1)
    queue.put({"profile": profile})
    try:
        with open('user_profiles/' + profile, 'r') as file:
            for line in file:
                parts = line.strip().split(':', 1)
                if len(parts) == 2:
                    function_name = parts[0]
                    params_str = parts[1]

                    param_list = params_str.split(',')
                    try:
                        params = [ast.literal_eval(param.strip()) for param in param_list]
                    except (ValueError, SyntaxError):
                        print(f"Error parsing parameters for {function_name}")
                        continue

                    if function_name in globals():
                        func = globals()[function_name]
                        if callable(func):
                            try:
                                time.sleep(0.1)
                                queue.put({"action": line})
                                if function_name == "start_profile":
                                    func(*params, queue)
                                else:
                                    func(*params)
                            except TypeError as e:
                                logging.error('Неверно указаны параметры команды - {}'.format(e))
                                sys.exit()
                        else:
                            print(f"{function_name} is not callable")
                    else:
                        print(f"Function {function_name} not found")
                else:
                    print(f"Invalid line format: {line.strip()}")

    except FileNotFoundError as e:
        logging.error("Файл конфигурации не найден")
        sys.exit()

    time.sleep(0.1)
    queue.put({"work": 0})
    time.sleep(0.1)
    queue.put({"profile": "None"})
    time.sleep(0.1)
    queue.put({"action": "-"})