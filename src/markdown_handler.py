import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # only split plain text nodes
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: unmatchted delimiter {delimiter!r} in {node.text!r}"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        img_matches = extract_markdown_images(node.text)
        if not img_matches:
            new_nodes.append(node)
            continue
        text = node.text
        for alt, url in img_matches:
            img_str = f"![{alt}]({url})"
            before, after = text.split(img_str, maxsplit=1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        link_matches = extract_markdown_links(node.text)
        if not link_matches:
            new_nodes.append(node)
            continue
        text = node.text
        for name, url in link_matches:
            link_str = f"[{name}]({url})"
            before, after = text.split(link_str, maxsplit=1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(name, TextType.LINK, url))
            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
