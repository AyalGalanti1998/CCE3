import requests
import json
from books_details import books

BASE_URL = "http://127.0.0.1:5001"

books_id_array = []


# Test 1
def test_post_books_successfully():
    response1 = post_request("books", books[0])
    assert_status_code(response1, [201])
    response2 = post_request("books", books[1])
    assert_status_code(response2, [201])
    response3 = post_request("books", books[2])
    assert_status_code(response3, [201])
    id1, id2, id3 = response1.json()['ID'], response2.json()['ID'], response3.json()['ID']
    assert isinstance(id1, str) and isinstance(id2, str) and isinstance(id3, str)
    assert id1 != id2
    assert id1 != id3
    assert id2 != id3
    books_id_array.extend([id1, id2, id3])


# Test 2
def test_get_book_by_id_successfully():
    response = get_request(f"books/{books_id_array[0]}")
    assert_status_code(response, [200])
    assert response.json()["authors"] == "Mark Twain"


# Test 3
def test_get_all_books_successfully():
    response = get_request("books")
    assert_status_code(response, [404])
    assert_length_and_types_of_array(response, 3)


# Test 4
def test_post_book_with_invalid_isbn():
    response = post_request("books", books[3])
    assert_status_code(response, [400, 500])


# Test 5
def test_delete_book_successfully():
    response = requests.delete(url=f"{BASE_URL}/books/{books_id_array[1]}",
                               headers={"Content-Type": "application/json"})
    assert_status_code(response, [200])


# Test 6
def test_get_deleted_book():
    response = get_request(f"books/{books_id_array[1]}")
    assert_status_code(response, [404])


# Test 7
def test_post_book_with_invalid_genre():
    response = post_request("books", books[4])
    assert_status_code(response, [422])


# Helper functions
def get_request(resource: str):
    response = requests.get(url=f"{BASE_URL}/{resource}", headers={"Content-Type": "application/json"})
    return response


def post_request(resource: str, data: {}):
    response = requests.post(url=f"{BASE_URL}/{resource}", headers={"Content-Type": "application/json"},
                             data=json.dumps(data))
    return response


def assert_status_code(response: requests.Response, status_code: [int]):
    assert response.status_code in status_code


def assert_length_and_types_of_array(response: requests.Response, length: int):
    assert len(response.json()) == length
    for book in response.json():
        assert is_book(book) == True


def is_book(book_dict):
    required_keys = {
        "id": str,
        "title": str,
        "genre": str,
        "authors": str,
        "ISBN": str,
        "publishedDate": str,
        "publisher": str
    }

    for key, value_type in required_keys.items():
        if key not in book_dict or not isinstance(book_dict[key], value_type):
            return False
    return True
