from hw.engine_stub import EngineStub
from hw.engine_wsad import EngineWsad
from settings.settings import Settings, EngineMode


class EngineFactory:

    @staticmethod
    def create_engine():
        if Settings.get_engine_mode() == EngineMode.USE_STUB:
            return EngineStub()
        else:
            return EngineWsad()
