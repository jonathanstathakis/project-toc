import pytest
from project_toc import build_toc
from pathlib import Path


@pytest.fixture
def notebook_path() -> Path:
    return Path("./tests/test_notebook.ipynb")


def test_toc(notebook_path: Path) -> None:
    toc = build_toc([notebook_path])

    assert not toc.empty
