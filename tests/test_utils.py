import pytest

from text_extractor.utils import resolve_file_type


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("document.pdf", "pdf"),
        ("report.DOCX", "docx"),
        ("data.csv", "csv"),
        ("notes.txt", "txt"),
        ("image.PNG", "png"),
        ("photo.jpg", "jpg"),
        ("snapshot.JPEG", "jpg"),
    ],
)
def test_resolve_file_type_known_extensions(filename, expected):
    assert resolve_file_type(filename) == expected


def test_resolve_file_type_unknown_extension():
    with pytest.raises(ValueError) as exc:
        resolve_file_type("file.unknown")
    message = str(exc.value)
    assert ".unknown" in message
    assert "file.unknown" not in message
