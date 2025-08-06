from text_extractor.models import ExtractedText, PageText


def test_models_roundtrip():
    page = PageText(page_number=1, text="Hello", ocr=False)
    result = ExtractedText(text="Hello", file_type="txt", pages=[page])
    assert result.pages[0].page_number == 1
    assert result.pages[0].text == "Hello"
    assert result.file_type == "txt"
    assert result.text == "Hello"
    assert result.pages[0].ocr is False
