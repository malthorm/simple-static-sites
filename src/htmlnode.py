from dataclasses import dataclass
from typing import Self


@dataclass
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: list[Self] | None = None
    props: dict[str, str] | None = None

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
