from __future__ import annotations

import io
from pathlib import Path
import pytest
from loaders import load_courses


def test_load_courses_json_str() -> None:
    json_str = '[{"title": "Go", "category": "IT", "students": 10, "rating": 4.6, "price": 10}]'
    res = load_courses(json_str)
    assert len(res) == 1
    assert res[0]["title"] == "Go"


def test_load_courses_csv_str() -> None:
    csv_str = "title,category,students,rating,price\nRust,Systems,50,4.9,20"
    res = load_courses(csv_str)
    assert len(res) == 1
    assert res[0]["title"] == "Rust"


def test_load_courses_json_file_path(tmp_path: Path) -> None:
    p = tmp_path / "data.json"
    p.write_text('[{"title": "C++", "category": "dev", "students": 30, "rating": 4.7, "price": 15}]', encoding="utf-8")
    assert load_courses(p)[0]["title"] == "C++"


def test_load_courses_csv_file_path(tmp_path: Path) -> None:
    p = tmp_path / "data.csv"
    p.write_text("title,category,students,rating,price\nSQL,DB,80,4.5,12", encoding="utf-8")
    assert load_courses(p)[0]["title"] == "SQL"


def test_load_courses_io_stream() -> None:
    stream = io.StringIO('[{"title": "Java", "category": "dev", "students": 100, "rating": 4.5, "price": 20}]')
    assert load_courses(stream)[0]["title"] == "Java"


def test_load_courses_list_direct() -> None:
    raw = [{"title": "Kotlin", "category": "dev", "students": 40, "rating": 4.6, "price": 18}]
    assert load_courses(raw) == raw


def test_load_courses_unsupported_type() -> None:
    with pytest.raises(TypeError):
        load_courses(12345)