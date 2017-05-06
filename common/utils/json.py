from typing import Any

import simplejson


class JSON:

    @classmethod
    def stringify(cls, value: Any, indent=4):
        return simplejson.dumps(value, sort_keys=True, indent=indent, ensure_ascii=False)

    @classmethod
    def parse(cls, value: str):
        return simplejson.loads(value)
