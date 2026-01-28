from __future__ import annotations
from enum import StrEnum

from htmlnode import LeafNode


class TextType(StrEnum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    text = text_node.text
    url = text_node.url if text_node.url else ""
    match text_node.text_type:
        case "text":
            return LeafNode(None, text)
        case "bold":
            return LeafNode("b", text)
        case "italic":
            return LeafNode("i", text)
        case "code":
            return LeafNode("code", text)
        case "link":
            return LeafNode("a", text, {"href": url})
        case "image":
            return LeafNode("img", "", {"src": url, "alt": text})
        case _:
            raise ValueError("Invalid text type")
