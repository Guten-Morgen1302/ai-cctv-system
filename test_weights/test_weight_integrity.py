"""
Integrity checks for the bundled placeholder weight files.

These are small stand-ins committed so the weight-loading paths can be
exercised without shipping the real multi-megabyte checkpoints.
"""

from pathlib import Path

import pytest

WEIGHTS_ROOT = Path(__file__).resolve().parent

FRONTEND_WEIGHTS = [
    "person_detection_frontend_v1.0.pt",
    "pose_estimation_frontend_v1.0.pt",
]

BACKEND_WEIGHTS = [
    "face_detection_backend_v1.5.pt",
    "object_detection_backend_v2.0.pt",
]


@pytest.mark.parametrize("filename", FRONTEND_WEIGHTS)
def test_frontend_weight_exists(filename):
    assert (WEIGHTS_ROOT / "frontend" / filename).is_file()


@pytest.mark.parametrize("filename", BACKEND_WEIGHTS)
def test_backend_weight_exists(filename):
    assert (WEIGHTS_ROOT / "models" / filename).is_file()


@pytest.mark.parametrize(
    "path",
    [WEIGHTS_ROOT / "frontend", WEIGHTS_ROOT / "models"],
    ids=["frontend", "models"],
)
def test_no_empty_weight_files(path):
    """A zero-byte checkpoint means a broken download or a bad LFS pull."""
    for weight_file in path.glob("*.pt"):
        assert weight_file.stat().st_size > 0, f"{weight_file.name} is empty"


def test_every_expected_weight_is_accounted_for():
    """Guards against a weight being renamed without updating the loaders."""
    found = {p.name for p in WEIGHTS_ROOT.rglob("*.pt")}
    missing = set(FRONTEND_WEIGHTS + BACKEND_WEIGHTS) - found
    assert not missing, f"missing weight files: {sorted(missing)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
