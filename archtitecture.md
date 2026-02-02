           ┌─────────────────┐
           │  markdown files  │
           └────────┬────────┘
                    │  read text
                    ▼
        ┌───────────────────────────┐
        │ markdown_to_blocks(md)     │
        │  - split on blank lines    │
        │  - trim & clean whitespace │
        └────────┬──────────────────┘
                 │ blocks (strings)
                 ▼
     ┌──────────────────────────────┐
     │ block_to_block_type(block)   │
     └────────┬─────────────────────┘
              │
              ├─────────────┐
              │             │
              ▼             ▼
   ┌────────────────┐   ┌─────────────────────┐
   │ CODE block      │   │ Non-code block      │
   │ no inline parse │   │ inline parse        │
   └───────┬────────┘   └──────────┬──────────┘
           │                       │
           ▼                       ▼
┌────────────────────┐   ┌────────────────────────┐
│ LeafNode("code",..)│   │ text_to_textnodes(text) │
│ ParentNode("pre", )│   │  - images/links         │
└─────────┬──────────┘   │  - ` ** _ delimiters    │
          │              └──────────┬──────────────┘
          │                         │ TextNodes
          │                         ▼
          │              ┌──────────────────────────┐
          │              │ text_node_to_html_node() │
          │              └──────────┬──────────────┘
          │                         │ LeafNodes
          └───────────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │ ParentNode(tag,  │
                 │   children=...)  │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │ root <div> node  │
                 └────────┬─────────┘
                          ▼
                    node.to_html()
                          ▼
                    HTML string
                          ▼
                   write to public/
