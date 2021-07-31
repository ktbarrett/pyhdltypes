import sys

__all__ = ("Protocol", "runtime_checkable")

if sys.version_info < (3, 8):
    from typing_extensions import Protocol, runtime_checkable
else:
    from typing import Protocol, runtime_checkable
