from RestrictedPython import PrintCollector
from RestrictedPython.Guards import guarded_setattr, safe_globals

from app.route.execute.exception.input_size_matching_error import InputSizeMatchingError
from app.web.exception.enum.error_enum import ErrorEnum


class RestrictedPythonConfig:

    def __init__(self, user_input):
        self.input_values = user_input.rstrip().split("\n")
        self.cur_input_index = 0

        self.limited_locals = {}

    def get_limited_locals(self):
        return self.limited_locals

    def get_limited_globals(self):
        restricted_globals = safe_globals.copy()

        if not restricted_globals:
            return restricted_globals

        # 추가된 필드 설정
        builtins = restricted_globals.get("__builtins__")
        if builtins:
            builtins["type"] = type
            builtins["list"] = list
            builtins["map"] = map
            builtins["all"] = all
            builtins["any"] = any
            builtins["ascii"] = ascii
            builtins["bin"] = bin
            builtins["dict"] = dict
            builtins["filter"] = filter
            builtins["float"] = float
            builtins["format"] = format
            builtins["_getattr_"] = getattr
            builtins["max"] = max
            builtins["min"] = min
            builtins["set"] = set
            builtins["sum"] = sum
            builtins["super"] = super
            builtins["vars"] = vars

            builtins["input"] = self._input
            builtins["_getiter_"] = self._iter
            builtins["_print_"] = PrintCollector
            builtins["_setattr_"] = guarded_setattr

        return restricted_globals

    def _iter(self, obj):
        """객체가 반복 가능하면 반복자를 반환."""
        if hasattr(obj, "__iter__"):
            return iter(obj)

    def _input(self, prompt=None):
        if self.cur_input_index < len(self.input_values):
            if "_print" in self.limited_locals:
                print_collector = self.limited_locals["_print"]
            else:
                print_collector = None

            if prompt and print_collector:
                print_collector.write(prompt)

            input_value = self.input_values[self.cur_input_index]
            self.cur_input_index += 1

            return input_value
        else:
            raise InputSizeMatchingError(ErrorEnum.INPUT_SIZE_MATCHING_ERROR)
