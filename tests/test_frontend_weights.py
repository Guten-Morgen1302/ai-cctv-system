"""
    # test_frontend_weights.py
    Checks that the weight files the frontend analytics views depend on are
    present and loadable before the dashboards are built.
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestFrontendIntegration(unittest.TestCase):
    """Integration tests for frontend components with test weights"""

    def setUp(self):
        self.frontend_weights = REPO_ROOT / "test_weights" / "frontend"
        self.model_weights = REPO_ROOT / "test_weights" / "models"

    def test_all_frontend_weights_available(self):
        for name in (
            "person_detection_frontend_v1.0.pt",
            "pose_estimation_frontend_v1.0.pt",
        ):
            with self.subTest(weight=name):
                self.assertTrue((self.frontend_weights / name).is_file())

    def test_all_backend_weights_available(self):
        for name in (
            "face_detection_backend_v1.5.pt",
            "object_detection_backend_v2.0.pt",
        ):
            with self.subTest(weight=name):
                self.assertTrue((self.model_weights / name).is_file())

    def test_weight_files_not_empty(self):
        for weight_file in self.frontend_weights.glob("*.pt"):
            with self.subTest(weight=weight_file.name):
                self.assertGreater(weight_file.stat().st_size, 0)

    def test_per_app_weight_directories_exist(self):
        """Each frontend app ships its own analytics weight alongside src/."""
        for app in ("DirectoryManager", "LandingPage", "blockchain"):
            with self.subTest(app=app):
                self.assertTrue((REPO_ROOT / "frontend" / app / "weights").is_dir())


if __name__ == "__main__":
    unittest.main()
