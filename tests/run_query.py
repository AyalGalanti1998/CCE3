import requests
import json
from books_details import books
from tests import assn3_tests


def post_books(book_details):
    """Posts specific book details to a server endpoint.

    Args:
        book_details (list): A list of dictionaries containing book details.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the POST request.
    """

    for index in [0, 1, 2, 5, 6, 7]:  # Select specific book indexes (adjusted for 0-based indexing)
        try:
            book = books[index]  # Access book details using index
            response = assn3_tests.post_request("books", book)
            response.raise_for_status()  # Raise an HTTPError on bad status code
        except requests.exceptions.RequestException as e:
            error_message = f"Error posting book: {book['title']}. {e}"
            print(error_message)  # Specific error handling


# Function to read queries from the file
def read_queries(file_path):
    with open(file_path, 'r') as file:
        queries = file.readlines()
    return [query.strip() for query in queries]


# Function to make HTTP GET requests with the queries
def make_requests(queries):
    responses = []
    for query in queries:
        try:
            response = assn3_tests.get_request(f"books{query}")
            response.raise_for_status()  # Raise an HTTPError on bad status
            responses.append(response.text)
        except requests.exceptions.RequestException as e:
            responses.append(f"error {response.status_code}")

    return responses


# Function to save responses to a file
def save_responses(file_path, responses):
    with open(file_path, 'w') as file:
        for i, response in enumerate(responses):
            file.write(f"query: qs-{i}" + "\n")
            file.write(f"response: {response}" + "\n")


# Main function to read queries, make requests, and save responses
def main():
    post_books()
    queries_file = '../query.txt'
    responses_file = 'response.txt'
    queries = read_queries(queries_file)
    responses = make_requests(queries)
    save_responses(responses_file, responses)


if __name__ == "__main__":
    main()