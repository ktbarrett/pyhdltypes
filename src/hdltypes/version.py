major = "0"
minor = "2"
patch = "0"
release = "dev0"

__version__ = f"{major}.{minor}.{patch}"

if release != "":  # pragma: no cover
    __version__ += f".{release}"
