"""srt_tools package."""

from importlib.metadata import version

__version__ = version("srt_tools")
__license__ = "CC0-1.0"

from .bom import read_text, write_text
from .core import Srt, SrtEntry

__all__ = ["read_text", "write_text", "Srt", "SrtEntry"]
