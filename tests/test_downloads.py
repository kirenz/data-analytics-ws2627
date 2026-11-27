from pathlib import Path
from unittest import TestCase
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


class DownloadTests(TestCase):
    def test_archives_contain_readable_uv_projects(self):
        for filename, project in (("agents-lab.zip", "agents-lab"), ("statistik-lab.zip", "statistik")):
            with self.subTest(filename=filename), ZipFile(ROOT / "downloads" / filename) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn(f"{project}/pyproject.toml", archive.namelist())
                self.assertIn(f"{project}/uv.lock", archive.namelist())

    def test_agents_lab_download_matches_sources(self):
        with ZipFile(ROOT / "downloads" / "agents-lab.zip") as archive:
            for name in archive.namelist():
                with self.subTest(name=name):
                    self.assertTrue(name.startswith("agents-lab/"))
                    self.assertNotIn("..", Path(name).parts)
                    self.assertNotIn(".env", Path(name).parts)
                    self.assertTrue(archive.read(name) == (ROOT / name).read_bytes())
