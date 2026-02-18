from PySide6.QtCore import QObject, Signal, Slot
import numpy as np
from src.backend.processor import ImageProcessor

#/////////////////////////////////#
#     AI ASYNC TASK WORKER        #
#/////////////////////////////////#

class AIWorker(QObject):
    finished = Signal(object, object)
    progress = Signal(int)
    error = Signal(str)

    @Slot(object, str)
    def run_ocr(self, cv_img, language):
        try:
            mask = ImageProcessor.run_ocr_logic(cv_img, language)
            self.finished.emit(mask, None)
        except Exception as e:
            self.error.emit(str(e))

    @Slot(object, object, int)
    def run_clean(self, cv_img, mask_img, max_tile_w):
        try:
            result, patches = ImageProcessor.run_clean_logic(
                cv_img, 
                mask_img, 
                max_tile_w, 
                progress_callback=self.progress.emit
            )
            self.finished.emit(result, patches)
        except Exception as e:
            self.error.emit(str(e))