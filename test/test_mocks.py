from __future__ import annotations

import contextlib
import datetime
import itertools
from typing import Callable


def mock_uuid_sequence(prefix: str = "00000000-0000-0000-0000-", start: int = 1):
    """
    Mock the UUID helper used throughout the Proligent model layer.
    This is needed so that the GUIDs "randomly generated" for tests match what we have in the "expected" files.

    Args:
        prefix: Prefix applied to each generated identifier.
        start: Starting integer suffix value.

    Returns:
        Context manager that patches UUID generation for the duration of the block.
    """

    from proligent import model as model_module
    util_uuid_descriptor = model_module.Util.__dict__["uuid"]
    is_staticmethod = isinstance(util_uuid_descriptor, staticmethod)
    util_uuid_func = (
        util_uuid_descriptor.__func__ if is_staticmethod else util_uuid_descriptor
    )

    counter = itertools.count(start)

    def _next_uuid() -> str:
        return f"{prefix}{next(counter):012d}"

    if is_staticmethod:

        def _fake_uuid(_supplier: Callable[[], str] = _next_uuid) -> str:
            return _supplier()

    else:

        def _fake_uuid(self, _supplier: Callable[[], str] = _next_uuid) -> str:
            return _supplier()

    @contextlib.contextmanager
    def _manager():
        original_code = util_uuid_func.__code__
        original_defaults = util_uuid_func.__defaults__
        original_kwdefaults = util_uuid_func.__kwdefaults__
        try:
            util_uuid_func.__code__ = _fake_uuid.__code__
            util_uuid_func.__defaults__ = _fake_uuid.__defaults__
            util_uuid_func.__kwdefaults__ = _fake_uuid.__kwdefaults__
            yield
        finally:
            util_uuid_func.__code__ = original_code
            util_uuid_func.__defaults__ = original_defaults
            util_uuid_func.__kwdefaults__ = original_kwdefaults

    return _manager()


def mock_util_timezone(timezone: str):
    """
    Temporarily override the Util timezone so scenarios can force specific offsets.
    """

    from proligent import model as model_module

    @contextlib.contextmanager
    def _manager():
        original_timezone = model_module.UTIL.timezone
        try:
            model_module.UTIL.timezone = timezone
            yield
        finally:
            model_module.UTIL.timezone = original_timezone

    return _manager()


def mock_datetime_now(frozen: datetime.datetime):
    """
    Patch datetime.datetime.now (and utcnow) used by the model layer.
    This is needed so that the "now datetime generated for tests match what we have in the "expected" files.
    """

    from proligent import model as model_module

    def _apply_timezone(value: datetime.datetime, tz):
        if tz is None:
            return value
        if value.tzinfo is not None:
            return value.astimezone(tz)
        if hasattr(tz, "localize"):
            return tz.localize(value)
        return value.replace(tzinfo=tz)

    original_datetime_type = datetime.datetime

    class FrozenDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return _apply_timezone(frozen, tz)

        @classmethod
        def utcnow(cls):
            utc_value = frozen
            if utc_value.tzinfo is not None:
                utc_value = utc_value.astimezone(datetime.timezone.utc)
            return utc_value.replace(tzinfo=None)

    def _constant_factory(value=frozen) -> datetime.datetime:
        return value

    def _is_datetime_now(factory: Callable[[], datetime.datetime]) -> bool:
        return (
            callable(factory)
            and getattr(factory, "__self__", None) is original_datetime_type
            and getattr(factory, "__name__", "") == "now"
        )

    @contextlib.contextmanager
    def _manager():
        datetime_module = datetime
        original_datetime = datetime_module.datetime
        original_model_datetime = model_module.datetime.datetime
        patched_cells: list[tuple[object, Callable[[], datetime.datetime]]] = []
        seen_cells: set[int] = set()
        try:
            datetime_module.datetime = FrozenDateTime
            model_module.datetime.datetime = FrozenDateTime
            for attr in model_module.__dict__.values():
                init_func = getattr(attr, "__init__", None)
                if not init_func or not getattr(init_func, "__closure__", None):
                    continue
                code = getattr(init_func, "__code__", None)
                if not code:
                    continue
                for name, cell in zip(code.co_freevars, init_func.__closure__):
                    if not name.startswith("__dataclass_dflt_"):
                        continue
                    cell_id = id(cell)
                    if cell_id in seen_cells:
                        continue
                    factory = cell.cell_contents
                    if _is_datetime_now(factory):
                        seen_cells.add(cell_id)
                        patched_cells.append((cell, factory))
                        cell.cell_contents = _constant_factory
            yield
        finally:
            datetime_module.datetime = original_datetime
            model_module.datetime.datetime = original_model_datetime
            for cell, factory in patched_cells:
                cell.cell_contents = factory

    return _manager()
