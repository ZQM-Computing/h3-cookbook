"""Runtime tests for the H3 cookbook examples."""

import os
import subprocess
import sys
from pathlib import Path

import h3
import pytest

ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = ROOT / "examples"
EXAMPLES = sorted(EXAMPLES_DIR.glob("*/run.py"))
EXPECTED_EXAMPLES = {
    "01-indexing",
    "02-aggregation",
    "03-visualization",
    "04-comparison",
    "05-duckdb-integration",
    "06-performance",
}


def test_exact_example_inventory() -> None:
    """Every advertised example has exactly one non-empty Python entry point."""
    actual = {path.parent.name for path in EXAMPLES}
    assert actual == EXPECTED_EXAMPLES, (
        f"Example inventory mismatch. Missing: {sorted(EXPECTED_EXAMPLES - actual)}; "
        f"unexpected: {sorted(actual - EXPECTED_EXAMPLES)}"
    )
    for example in EXAMPLES:
        assert example.is_file() and example.stat().st_size > 0, f"Missing or empty entry point: {example}"


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
        ("02-aggregation", "Aggregated point count: 1000"),
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
    assert expected_output in result.stdout, (
        f"{example_name} did not print its expected output marker {expected_output!r}. stdout:\n{result.stdout}"
    )
    if example_name == "02-aggregation":
        assert "Total points: 1000" in result.stdout
        totals = {
            line.split(":", 1)[0]: int(line.split(":", 1)[1].strip())
            for line in result.stdout.splitlines()
            if line.startswith(("Input value sum:", "Aggregated value sum:"))
        }
        assert totals["Input value sum"] == totals["Aggregated value sum"], (
            f"Aggregation changed the total value: {totals}"
        )
    if example_name == "03-visualization":
        assert "Saved to h3_heatmap.png" in result.stdout


def test_h3_indexing_round_trip_and_boundary() -> None:
    """A point's H3 cell centroid re-indexes to the same cell and has a valid boundary."""
    latitude, longitude, resolution = 29.02, -80.93, 9
    cell = h3.latlng_to_cell(latitude, longitude, resolution)
    center_latitude, center_longitude = h3.cell_to_latlng(cell)
    assert h3.latlng_to_cell(center_latitude, center_longitude, resolution) == cell

    boundary = h3.cell_to_boundary(cell)
    assert len(boundary) >= 5, f"Expected a valid H3 boundary, got {len(boundary)} vertices"
    for vertex_latitude, vertex_longitude in boundary:
        assert -90 <= vertex_latitude <= 90
        assert -180 <= vertex_longitude <= 180


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
    """Compile every Python example in memory without leaving bytecode artifacts."""
    for py_file in EXAMPLES:
        source = py_file.read_text(encoding="utf-8")
        compile(source, str(py_file.relative_to(ROOT)), "exec")


@pytest.mark.parametrize("required_file", ["README.md", "LICENSE"])
def test_repository_metadata_exists(required_file: str) -> None:
    """Core repository metadata files are present."""
    assert (ROOT / required_file).is_file()
