import requests
from books_details import books
import assn3_tests


def post_books():
    """Posts specific book details to a server endpoint.
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


def process_queries(input_file_path, output_file_path):
    # Step 1: Read queries from the input file
    with open(input_file_path, 'r') as file:
        queries = [query.strip() for query in file.readlines()]

    # Step 2: Make HTTP GET requests with the queries
    responses = []
    for query in queries:
        try:
            response = assn3_tests.get_request(f"books{query}")
            response.raise_for_status()  # Raise an HTTPError on bad status
            responses.append((query,response.text))
        except requests.exceptions.RequestException as e:
            responses.append((query,f"error {response.status_code}"))

    # Step 3: Save responses to the output file
    with open(output_file_path, 'w') as file:
        for query, response in responses:
            file.write(f"query: {query}\n")
            file.write(f"response: {response}\n")


# Main function to read queries, make requests, and save responses
def main():
    post_books()
    queries_file = '../query.txt'
    responses_file = 'response.txt'
    process_queries(queries_file, responses_file)

if __name__ == "__main__":
    main()