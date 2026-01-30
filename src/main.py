# import markdown_handler
# from textnode import TextNode, TextType
from utils import make_clean_public, copy_content


def main():
    make_clean_public()
    copy_content("./static/", "./public/")


main()
