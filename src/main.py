import markdown_handler
from textnode import TextNode, TextType


def main():
    md = """
# H1 heading

This is **bolded** paragraph
text in a p
tag here

## H2 Heading

This is another paragraph with _italic_ text and `inline code` here

Now follows a code block:

```
Ignore **inline markdown** like this
x = x + 1
y = x - 1
x == y
```

This is a paragraph with an [inline link](www.url.de)

> Also blockquotes
> are something else
> Malte
"""
    md = """
# Title

## Intro

Here is some paragraph

###### This just be an h6

####### This has too many #s, so it's a paragraph
"""

    md = r"""
# Title

## Intro

Here is some paragraph

###### This just be an h6

![Vivavis Background](C:\Users\u17275\Pictures\vivavis-background.jpg)

[google](https://www.google.com)
"""

    md = r"""
# Ordered List

1. first
2. second
3. third
"""
    md = r"""
# Ordered List

- first
- second
- third
"""
    html = markdown_handler.markdown_to_html_node(md).to_html()
    print(html)


main()
