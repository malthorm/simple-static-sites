import unittest
import tempfile
from pathlib import Path

from main import generate_pages_recursive
from utils import copy_static


class TestSiteGeneration(unittest.TestCase):
    def test_generate_pages_recursive_creates_expected_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            content = root / "content"
            public = root / "public"
            content.mkdir()
            (content / "blog" / "tom").mkdir(parents=True)

            (content / "index.md").write_text("# Home\n\nHello", encoding="utf-8")
            (content / "blog" / "tom" / "index.md").write_text(
                "# Tom\n\nPost", encoding="utf-8"
            )

            template = root / "template.html"
            template.write_text(
                "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>",
                encoding="utf-8",
            )

            generate_pages_recursive(content, template, public)

            self.assertTrue((public / "index.html").exists())
            self.assertTrue((public / "blog" / "tom" / "index.html").exists())
            self.assertFalse((public / "index.md").exists())

    def test_generated_html_contains_title_and_rendered_content(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            content = root / "content"
            public = root / "public"
            content.mkdir()

            (content / "index.md").write_text(
                "# My Title\n\nThis is **bold**.", encoding="utf-8"
            )
            template = root / "template.html"
            template.write_text("<h1>{{ Title }}</h1>{{ Content }}", encoding="utf-8")

            generate_pages_recursive(content, template, public)

            out = (public / "index.html").read_text(encoding="utf-8")
            self.assertIn("<h1>My Title</h1>", out)
            self.assertIn("<b>bold</b>", out)

    def test_template_reuse_does_not_leak_between_pages(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            content = root / "content"
            public = root / "public"
            content.mkdir()

            (content / "a.md").write_text("# A\n\nHello", encoding="utf-8")
            (content / "b.md").write_text("# B\n\nWorld", encoding="utf-8")

            template = root / "template.html"
            template.write_text(
                "<title>{{ Title }}</title>{{ Content }}", encoding="utf-8"
            )

            generate_pages_recursive(content, template, public)

            a = (public / "a.html").read_text(encoding="utf-8")
            b = (public / "b.html").read_text(encoding="utf-8")

            self.assertIn("<title>A</title>", a)
            self.assertNotIn("<title>B</title>", a)
            self.assertIn("<title>B</title>", b)
            self.assertNotIn("<title>A</title>", b)

    def test_copy_static_cleans_destination_and_copies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            static = root / "static"
            public = root / "public"
            static.mkdir()
            public.mkdir()

            # existing generated junk should be deleted
            (public / "old.txt").write_text("old", encoding="utf-8")

            # new static content should be copied (including nested dirs)
            (static / "index.css").write_text("body {}", encoding="utf-8")
            (static / "images").mkdir()
            (static / "images" / "tolkien.png").write_bytes(
                b"\x89PNG\r\n\x1a\n"
            )  # tiny fake png header

            copy_static(str(static), str(public))

            self.assertFalse((public / "old.txt").exists())
            self.assertTrue((public / "index.css").exists())
            self.assertTrue((public / "images" / "tolkien.png").exists())


if __name__ == "__main__":
    unittest.main()
