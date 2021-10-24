from pydantic import BaseSettings
from pathlib import Path, PurePath


class Config(BaseSettings):
    # plugin custom config
    setupath: Path = PurePath()
    realpath: Path = PurePath()
    wallpaperpath: Path = PurePath()

    class Config:
        extra = "ignore"
