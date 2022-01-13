from typing import Any, TypeVar

from frozenlist import FrozenList
from typing_extensions import Protocol

__version__ = "1.2.0"

__all__ = ("Signal",)


_Args = TypeVar("_Args", contravariant=True)
_KWArgs = TypeVar("_KWArgs", contravariant=True)


class _Func(Protocol[_Args, _KWArgs]):
    async def __call__(self, *args: _Args, **kwargs: _KWArgs) -> None:
        pass


class Signal(FrozenList[_Func[_Args, _KWArgs]]):
    """Coroutine-based signal implementation.

    To connect a callback to a signal, use any list method.

    Signals are fired using the send() coroutine, which takes named
    arguments.
    """

    __slots__ = ("_owner",)

    def __init__(self, owner: Any) -> None:
        super().__init__()
        self._owner = owner

    def __repr__(self) -> str:
        return "<Signal owner={}, frozen={}, {!r}>".format(
            self._owner, self.frozen, list(self)
        )

    async def send(self, *args: _Args, **kwargs: _KWArgs) -> None:
        """
        Sends data to all registered receivers.
        """
        if not self.frozen:
            raise RuntimeError("Cannot send non-frozen signal.")

        for receiver in self:
            await receiver(*args, **kwargs)
