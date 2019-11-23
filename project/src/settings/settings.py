from enum import Enum


class EngineMode(Enum):
    USE_WSAD = 0
    USE_STUB = 1


class Settings:
    __engineMode: EngineMode = EngineMode.USE_WSAD

    @staticmethod
    def set_engine_mode(mode: EngineMode):
        Settings.__engineMode = mode

    @staticmethod
    def get_engine_mode():
        return Settings.__engineMode
