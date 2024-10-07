from RestrictedPython import PrintCollector
from RestrictedPython.Guards import guarded_setattr, safe_globals

from app.route.execute.exception.code_execute_error import CodeExecuteError
from app.web.exception.enum.error_enum import ErrorEnum


class LimitEnv:

    def __init__(self, input_values):
        self.input_values = input_values
        self.cur_input_index = 0

        self.limited_locals = {}
        self.limited_globals = self._set_limited_globals()

    def _set_limited_globals(self):
        restricted_globals = safe_globals.copy()

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

             # prompt가 주어지면 PrintCollector를 통해 출력
            if prompt and print_collector:
                print_collector.write(prompt)

            input_value = self.input_values[self.cur_input_index]
            self.cur_input_index += 1

            return input_value
        else:
            raise CodeExecuteError(ErrorEnum.INPUT_SIZE_MATCHING_ERROR)
