"""
Fire and smoke detection.

Wraps the two trained YOLO checkpoints in weights/ behind one interface.
The checkpoints are not committed (they are ~84 MB), so every path here
degrades to "disabled" rather than raising when they are absent.

Inference is throttled: fire and smoke develop over seconds, not frames,
so running the extra two models on every frame would cost throughput for
no detection benefit.
"""

import logging
import os
import threading

logger = logging.getLogger(__name__)

# Defaults point at the newest checkpoint of each kind. Override with
# FIRE_WEIGHTS / SMOKE_WEIGHTS to test a different training run.
DEFAULT_FIRE_WEIGHTS = os.path.join("weights", "trained_fire_dataset_V2.1.pt")
DEFAULT_SMOKE_WEIGHTS = os.path.join("weights", "[25_epochs]trained_smoke_V1.1.pt")


class FireSmokeDetector:
    """Runs the fire and smoke checkpoints over frames on a fixed interval."""

    def __init__(self, fire_weights=None, smoke_weights=None,
                 confidence=0.45, frame_interval=10):
        self.fire_weights = fire_weights or os.getenv("FIRE_WEIGHTS", DEFAULT_FIRE_WEIGHTS)
        self.smoke_weights = smoke_weights or os.getenv("SMOKE_WEIGHTS", DEFAULT_SMOKE_WEIGHTS)
        self.confidence = confidence
        self.frame_interval = max(1, frame_interval)

        self.fire_model = None
        self.smoke_model = None
        self.enabled = False

        self._frame_counter = 0
        self._last_detections = []
        self._lock = threading.Lock()

        self._load_models()

    def _load_models(self):
        """Load whichever checkpoints are present. Missing ones stay None."""
        try:
            from ultralytics import YOLO
        except ImportError:
            logger.warning("ultralytics unavailable; fire/smoke detection disabled")
            return

        for attr, path, label in (
            ("fire_model", self.fire_weights, "fire"),
            ("smoke_model", self.smoke_weights, "smoke"),
        ):
            if not os.path.exists(path):
                logger.warning(
                    "%s weights not found at %s; %s detection disabled. "
                    "Download the checkpoint or set %s_WEIGHTS.",
                    label.capitalize(), path, label, label.upper(),
                )
                continue
            try:
                setattr(self, attr, YOLO(path))
                logger.info("%s model loaded from %s", label.capitalize(), path)
            except Exception as e:
                logger.error("Failed to load %s model: %s", label, e)

        self.enabled = self.fire_model is not None or self.smoke_model is not None

    def detect(self, frame):
        """
        Return [{'type', 'confidence', 'bbox'}] for fire/smoke in this frame.

        Only every Nth frame is actually run through the models; in between
        the previous result is returned so overlays do not flicker.
        """
        if not self.enabled or frame is None:
            return []

        with self._lock:
            self._frame_counter += 1
            if self._frame_counter % self.frame_interval != 0:
                return list(self._last_detections)

        detections = []
        for model, label in ((self.fire_model, "fire"), (self.smoke_model, "smoke")):
            if model is None:
                continue
            try:
                result = model(frame, verbose=False, conf=self.confidence)[0]
                for box in result.boxes:
                    detections.append({
                        "type": label,
                        "confidence": float(box.conf[0]),
                        "bbox": [int(v) for v in box.xyxy[0].tolist()],
                    })
            except Exception as e:
                logger.error("%s inference failed: %s", label, e)

        with self._lock:
            self._last_detections = detections
        return detections

    @staticmethod
    def highest_confidence(detections, hazard_type):
        """Best confidence for one hazard type, or 0.0 if it was not seen."""
        scores = [d["confidence"] for d in detections if d["type"] == hazard_type]
        return max(scores) if scores else 0.0
