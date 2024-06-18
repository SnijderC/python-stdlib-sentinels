"""
Copyright © 2021-2022 Tal Einat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

This code is a copy from https://github.com/taleinat/python-stdlib-sentinels.
"""

import sys as _sys
from threading import Lock
from types import FrameType
from typing import Dict, Optional, Self, cast, final

__all__ = ["Sentinel"]


@final
class Sentinel:
    """Create a unique sentinel object.

    *name* should be the fully-qualified name of the variable to which the
    return value shall be assigned.

    *repr*, if supplied, will be used for the repr of the sentinel object.
    If not provided, "<name>" will be used (with any leading class names
    removed).

    *bool_value* is the value (True/False) used for the sentinel object in
    boolean contexts.

    *module_name*, if supplied, will be used instead of inspecting the call
    stack to find the name of the module from which
    """

    _name: str
    _repr: str
    _module_name: str
    _bool_value: bool

    def __new__(
        cls,
        name: str,
        repr: Optional[str] = None,
        bool_value: bool = True,
        module_name: Optional[str] = None,
    ) -> Self | "Sentinel":
        name = str(name)
        repr = repr or f'<{name.split(".")[-1]}>'
        bool_value = bool(bool_value)
        if not module_name:
            try:
                module_name = cast(str, _get_parent_frame().f_globals.get("__name__", "__main__"))
            except (AttributeError, ValueError):
                module_name = __name__

        registry_key = _sys.intern(f"{module_name}-{name}")
        with _lock:
            sentinel = _registry.get(registry_key, None)
            if sentinel is None:
                sentinel = super().__new__(cls)
                sentinel._name = name
                sentinel._repr = repr
                sentinel._bool_value = bool_value
                sentinel._module_name = module_name

                _registry[registry_key] = sentinel

        return sentinel

    def __repr__(self):
        return self._repr

    def __bool__(self):
        return self._bool_value

    def __reduce__(self):
        return (
            self.__class__,
            (
                self._name,
                self._repr,
                self._bool_value,
                self._module_name,
            ),
        )


_lock = Lock()
_registry: Dict[str, Sentinel] = {}


def _get_parent_frame() -> FrameType:  # type: ignore
    """Return the frame object for the caller's parent stack frame."""
    return _sys._getframe(2)


del Lock, final, Dict, Optional
