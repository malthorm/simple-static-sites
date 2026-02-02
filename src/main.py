from pathlib import Path

from markdown_handler import markdown_to_html_node, extract_title
from utils import copy_static


def generate_page(from_path: str, template_path: str, dest_path) -> None:
    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )
    with open(from_path) as md_src:
        md = md_src.read()
    with open(template_path) as template_src:
        template = template_src.read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    with open(dest_path, "w") as index_html:
        index_html.write(template)


def main() -> None:
    project_root = Path(__file__).parent.parent
    static_dir = str(project_root / "static")
    public_dir = str(project_root / "public")
    content_dir = str(project_root / "content")

    copy_static(static_dir, public_dir)
    generate_page(
        content_dir + "/index.md",
        str(project_root) + "/template.html",
        public_dir + "/index.html",
    )


if __name__ == "__main__":
    main()
