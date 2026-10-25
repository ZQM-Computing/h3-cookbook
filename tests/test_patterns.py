"""Runtime tests for the H3 cookbook examples."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = ROOT / "examples"
EXAMPLES = sorted(EXAMPLES_DIR.glob("*/run.py"))


def run_example(example: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Execute one documented example and capture its output."""
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    try:
        return subprocess.run(
            [sys.executable, str(example)],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=90,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise AssertionError(
            f"Example {example.relative_to(ROOT)} failed with exit code {exc.returncode}.\n"
            f"stdout:\n{exc.stdout or '<empty>'}\nstderr:\n{exc.stderr or '<empty>'}"
        ) from exc


@pytest.mark.parametrize(
    ("example_name", "expected_output"),
    [
        ("01-indexing", "H3 cell:"),
        ("02-aggregation", "Total points: 1000"),
        ("03-visualization", "Saved to h3_grid.png"),
        ("04-comparison", "Boundary vertices:"),
        ("05-duckdb-integration", "Aggregation by H3 cell:"),
        ("06-performance", "Point-to-cell: 10000 points"),
    ],
)
def test_example_executes(tmp_path: Path, example_name: str, expected_output: str) -> None:
    """Run each example independently so failures identify the exact pattern."""
    example = EXAMPLES_DIR / example_name / "run.py"
    assert example.is_file(), f"Missing runnable example: {example.relative_to(ROOT)}"
    result = run_example(example, tmp_path)
    assert expected_output in result.stdout, f"{example_name} did not print its expected output marker {expected_output!r}. stdout:\n{result.stdout}"
    if example_name == "03-visualization":
        assert "Saved to h3_heatmap.png" in result.stdout


def test_visualization_outputs_are_valid_pngs(tmp_path: Path) -> None:
    """The visualization example creates non-empty PNG files."""
    example = EXAMPLES_DIR / "03-visualization" / "run.py"
    run_example(example, tmp_path)
    png_signature = b"\x89PNG\r\n\x1a\n"
    for filename in ("h3_grid.png", "h3_heatmap.png"):
        image = tmp_path / filename
        assert image.is_file(), f"Missing visualization output: {filename}"
        data = image.read_bytes()
        assert len(data) > 1_000, f"Visualization output is unexpectedly small: {filename}"
        assert data.startswith(png_signature), f"Invalid PNG signature: {filename}"


def test_examples_compile() -> None:
    """All Python examples compile independently."""
    for py_file in EXAMPLES:
        subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )


@pytest.mark.parametrize("required_file", ["README.md", "LICENSE"])
def test_repository_metadata_exists(required_file: str) -> None:
    """Core repository metadata files are present."""
    assert (ROOT / required_file).is_file()
