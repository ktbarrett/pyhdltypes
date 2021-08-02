major = "0"
minor = "1"
patch = "0"
release = ""

__version__ = f"{major}.{minor}.{patch}"

if release != "":  # pragma: no cover
    __version__ += f".{release}"
