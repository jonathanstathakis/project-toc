from pathlib import Path
from nbconvert import MarkdownExporter
import pandas as pd
from frontmatter import Frontmatter
from yaml.scanner import ScannerError
from yaml.parser import ParserError


class Notebook:
    def __init__(self, path):
        self.path = path
        self.attrs = self.get_attrs(path=self.path)
        self.attrs["filename"] = Path(self.path).stem
        self.attrs["link"] = f"[link]({Path(self.path)})"

    def get_attrs(self, path):
        fm = Frontmatter()
        md_exporter = MarkdownExporter()

        markdown = md_exporter.from_filename(path)

        frontmatter = markdown[0]

        try:
            attrs = fm.read(frontmatter)["attributes"]
        except (ScannerError, ParserError) as e:
            e.add_note(f"Error occured when parsing {path}")
            raise e

        if not attrs:
            attrs = {}

        return attrs


def build_toc(paths: list[Path]) -> pd.DataFrame:
    """
    Create a table of contents as a polars dataframe from querying over the ipynb in `path`.

    `path` is searched recursively.
    """
    attrs = []
    for path in paths:
        try:
            attrs.append(Notebook(str(path)).attrs)
        except NameError as e:
            e.add_note(str(path))
            raise e

    toc = pd.DataFrame.from_records(attrs)

    try:
        toc["cdt"] = pd.to_datetime(toc["cdt"])
        toc.sort_values("cdt", ascending=False)

    except KeyError:
        from warnings import warn

        warn("tried to sort by creation date but no key 'cdt' present")

    toc = pd.DataFrame(toc)

    return toc
