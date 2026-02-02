from __future__ import annotations

import logging
from pathlib import Path

from markdown_handler import extract_title, markdown_to_html_node
from utils import copy_static
from logger import logger

logging.basicConfig(
    filename="ssg.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


def generate_pages_recursive(
    content_dir: str | Path,
    template_path: str | Path,
    public_dir: str | Path,
) -> None:
    content_dir = Path(content_dir)
    template_path = Path(template_path)
    public_dir = Path(public_dir)

    template = template_path.read_text(encoding="utf-8")

    for md_path in content_dir.rglob("*.md"):
        rel = md_path.relative_to(content_dir)
        out_path = (public_dir / rel).with_suffix(".html")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        generate_page(md_path, template, out_path)


def generate_page(from_path: Path, template: str, dest_path: Path) -> None:
    logger.info(f"Generating page from '{from_path}' to '{dest_path}'")

    md = from_path.read_text(encoding="utf-8")
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_path.write_text(page, encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).parent.parent
    static_dir = project_root / "static"
    public_dir = project_root / "public"
    content_dir = project_root / "content"
    template_path = str(project_root) + "/template.html"

    copy_static(str(static_dir), str(public_dir))
    generate_pages_recursive(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()
