import pytest

from text_extractor import parser_factory
from text_extractor.parsers import pdf_parser, txt_parser


def test_select_parser_by_extension():
    parser = parser_factory.select_parser("sample.pdf")
    assert parser is pdf_parser.parse


def test_select_parser_by_mime():
    parser = parser_factory.select_parser("unknown.bin", mime_type="text/plain")
    assert parser is txt_parser.parse


def test_select_parser_unknown_extension():
    with pytest.raises(ValueError):
        parser_factory.select_parser("file.xyz")


def test_select_parser_unknown_mime():
    with pytest.raises(ValueError):
        parser_factory.select_parser("file", mime_type="application/unknown")
