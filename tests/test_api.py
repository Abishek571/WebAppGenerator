"""
Unit tests for document parser.
"""
import os
from utils.parser import parse_doc

def test_parse_txt():
    with open("test.txt", "w") as f:
        f.write("Hello world!")
    text = parse_doc("test.txt")
    assert "Hello world!" in text
    os.remove("test.txt")
