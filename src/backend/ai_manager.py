import os
import gc
from src.backend.onnx_engine import ONNXEngine
from src.utils.paths import Paths
from src.utils.logger import logger

#/////////////////////////////////#
#     AI MODEL RESOURCE MGMT      #
#/////////////////////////////////#

class AIManager:
    _ocr_engine = None
    _lama_engine = None
    _persistent_mode = False

    @staticmethod
    def set_persistence(enabled: bool):
        AIManager._persistent_mode = enabled
        if not enabled:
            AIManager.flush()

    @staticmethod
    def get_ocr():
        if not AIManager._persistent_mode:
            if AIManager._lama_engine is not None:
                AIManager._lama_engine = None
                gc.collect()

        if AIManager._ocr_engine is None:
            path = Paths.get_model("ocr.onnx")
            if os.path.exists(path):
                AIManager._ocr_engine = ONNXEngine(path)
            else:
                logger.error(f"[X] OCR Model Missing: {path}")
        return AIManager._ocr_engine

    @staticmethod
    def get_lama():
        if not AIManager._persistent_mode:
            if AIManager._ocr_engine is not None:
                AIManager._ocr_engine = None
                gc.collect()

        if AIManager._lama_engine is None:
            path = Paths.get_model("lama.onnx")
            if os.path.exists(path):
                AIManager._lama_engine = ONNXEngine(path)
            else:
                logger.error(f"[X] LaMa Model Missing: {path}")
        return AIManager._lama_engine

    @staticmethod
    def flush():
        AIManager._ocr_engine = None
        AIManager._lama_engine = None
        gc.collect()
        logger.info("[i] VRAM Flushed: Model Memory Released")