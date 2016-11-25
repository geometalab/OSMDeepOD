import pytest
from src.base.tag import Tag


@pytest.fixture(scope="function", autouse=True)
def tag():
    key = 'key'
    value = 'value'
    return Tag(key=key, value=value)


def test_new_tag(tag):
    assert tag.value == 'value'
    assert tag.key == 'key'


def test_tag_to_string(tag):
    assert str(tag) == 'key=value'
