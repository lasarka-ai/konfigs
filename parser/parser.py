import sys
import json
import re
import argparse

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def is_valid_name(self, name):
        return bool(re.match(r'^[a-z][a-z0-9_]*$', str(name)))

    def parse_value(self, value):
        if isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, dict):
            return self.parse_dict(value)
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return str(int(value))  # true -> 1, false -> 0
        else:
            raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")

    def parse_dict(self, data):
        result = []
        result.append("$[")
        items = []
        for key, value in data.items():
            if not self.is_valid_name(key):
                raise ValueError(f"Некорректное имя: {key}")
            items.append(f" {key} : {self.parse_value(value)}")
        result.append(",\n".join(items))
        result.append("]")
        return "\n".join(result)

    def parse_const(self, name, value):
        if not self.is_valid_name(name):
            raise ValueError(f"Некорректное имя константы: {name}")
        self.constants[name] = value
        return f"const {name} = {self.parse_value(value)}"

    def get_const_value(self, name):
        if name not in self.constants:
            raise ValueError(f"Константа {name} не найдена")
        return f"?({name})"

    def parse_input(self, data):
        result = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "const":
                    if isinstance(value, dict):
                        for const_name, const_value in value.items():
                            result.append(self.parse_const(const_name, const_value))
                    else:
                        raise ValueError("Поле 'const' должно быть словарем")
                elif key == "config":
                    if "comment" in value:
                        result.append(f"/*\n{value['comment']}\n*/")
                        del value["comment"]
                    result.append(self.parse_dict(value))
                else:
                    raise ValueError(f"Неизвестный ключ верхнего уровня: {key}")
        else:
            raise ValueError("Ожидался JSON объект на верхнем уровне")
        return "\n".join(result)

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', help='Входной JSON файл')
    arg_parser.add_argument('output', help='Выходной файл')
    args = arg_parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        parser = ConfigParser()
        result = parser.parse_input(input_data)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)

    except json.JSONDecodeError as e:
        print(f"Ошибка JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка файла: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
