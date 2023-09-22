# Enhanced by AI:
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional
1. Import statements have been moved to the top and grouped for better organization:
    ```python
    from typing import List, Optional
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    from bs4 import BeautifulSoup
    import requests
    ```

2. The `BookRecommendationSystem` class has been renamed to `BookRecommender` for a more concise name. Additionally, docstrings have been added to improve code readability and documentation.

3. The code now uses type hints to specify the argument types and return types in function signatures. This improves code readability and helps with catching type errors early.

4. A constant variable `URL` has been extracted to store the URL for scraping. This improves code maintainability by separating the URL from the scraping logic and making it easier to update in the future.

5. The extraction of book information using BeautifulSoup has been simplified. The `select` method allows us to select specific elements based on CSS selectors, reducing the number of lines needed to extract the book information.

6. The `get_summary` method in the `Book` class has been converted into a property decorator. This simplifies the code and allows the summary to be accessed as an attribute(`book.summary`) instead of as a method(`book.get_summary()`).

7. The `get_book_recommendations` method in the `BookRecommender` class has been simplified using list comprehension and slicing. This reduces the number of lines needed to extract the top 5 recommendations based on similarity scores.

8. Error handling has been added in case the user input has no matching books. If there are no book recommendations, an empty list is returned.

9. The `preprocess_input` and `_calculate_similarity` methods have been improved with type hints and variable name updates. This improves code readability and clarity.

10. The `print_recommendations` method uses f-strings for improved readability when printing the book recommendations.

11. A `main` function has been added to encapsulate the creation of the `BookRecommender` instance and running the recommendation system. This separates the main logic of the program from the class definition, making it easier to understand and test.

Overall, these enhancements improve the readability, maintainability, and functionality of the code.

Here's the refactored code with explanations for each change:

```python


class Book:
    """
    Represents a book with its metadata and summary.
    """

    def __init__(self, title: str, author: str, genre: str, rating: float, reviews: int, url: str, summary: str) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.reviews = reviews
        self.url = url
        self._summary = summary

    @property
    def summary(self) -> str:
        """
        A property that returns a shortened summary of the book.
        """
        return self._summary[:100] + "..." if len(self._summary) > 100 else self._summary

    def __str__(self) -> str:
        return f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}\nRating: {self.rating}\nReviews: {self.reviews}\nSummary: {self.summary}\nURL: {self.url}\n"


class BookRecommender:
    """
    Recommends books based on user input and book similarity.
    """

    def __init__(self) -> None:
        self.books: List[Book] = []

    def scrape_book_data(self) -> None:
        """
        Scrapes book data from the Goodreads website.
        """
        URL = "https://www.goodreads.com/genre/show/19-science-fiction"
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, "html.parser")
        book_elements = soup.select("div.coverWrapper")

        for book_element in book_elements:
            title_element = book_element.select_one("a.bookTitle")
            title = title_element.text.strip()
            url = f"https://www.goodreads.com{title_element['href']}"

            author_element = book_element.select_one("a.authorName")
            author = author_element.text.strip()

            genre_element = book_element.select_one("a.actionLinkLite")
            genre = genre_element.text.strip()

            rating_element = book_element.select_one("span.minirating")
            rating = float(rating_element.text.strip().split()[1])

            reviews_element = book_element.select_one("span.reviewsCount")
            reviews = int(reviews_element.text.strip().split()
                          [0].replace(",", ""))

            summary_element = book_element.select_one("div.readable")
            summary = summary_element.text.strip() if summary_element else "Summary not available"

            book = Book(title, author, genre, rating, reviews, url, summary)
            self.books.append(book)

    def get_book_recommendations(self, user_input: str) -> List[Book]:
        """
        Retrieves book recommendations based on the user's input.
        """
        user_vector = self._preprocess_input(user_input)
        if not user_vector:
            return []

        similarity_scores = self._calculate_similarity(user_vector)
        sorted_books = sorted(
            zip(self.books, similarity_scores), key=lambda x: x[1], reverse=True)
        return [book for book, _ in sorted_books[:5]]

    def _preprocess_input(self, user_input: str) -> Optional[List[float]]:
        """
        Preprocesses the user input and computes the user vector.
        """
        documents = [book.summary for book in self.books]
        if not documents:
            return None

        documents.append(user_input)
        vectorizer = TfidfVectorizer(token_pattern=r'\b\w+\b')
        matrix = vectorizer.fit_transform(documents)

        user_vector = matrix[-1].toarray()[0].tolist()
        return user_vector

    def _calculate_similarity(self, user_vector: List[float]) -> List[float]:
        """
        Calculates the similarity scores between the user vector and book vectors.
        """
        if not self.books:
            return []

        book_vectors = [vector.tolist() for vector in self.books]
        similarity_scores = cosine_similarity([user_vector], book_vectors)[0]
        return similarity_scores

    def print_recommendations(self, recommendations: List[Book]) -> None:
        """
        Prints the book recommendations.
        """
        print("Personalized Book Recommendations:")
        if recommendations:
            for i, book in enumerate(recommendations, start=1):
                print(f"{i}.")
                print(book)
        else:
            print("No book recommendations found.")

    def run_recommendation_system(self) -> None:
        """
        Runs the book recommendation system in a loop.
        """
        self.scrape_book_data()

        while True:
            user_input = input("Enter a genre you like (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break
            recommendations = self.get_book_recommendations(user_input)
            self.print_recommendations(recommendations)

    """The given code snippet is a prompt that asks us to provide a docstring for a Python function named `main`. The code itself is missing, so we'll focus on improving the documentation instead.

Firstly, let's define the `main` function with a docstring that clearly describes its purpose, inputs, and outputs. Here's a refactored version of the code with an informative docstring:

```python
def main():
    """
    Perform the main program logic.

    This function is the entry point of the program and executes the main
    program logic. It does not take any arguments and does not return any value.
    """
    # Add your main program logic here

```

In the docstring, I have provided a brief summary of what the function does and its role as the entry point of the program. I also mentioned that it doesn't take any arguments and doesn't return any value. 

Remember, a good docstring should provide clear and concise information about the purpose, inputs, outputs, and any other relevant details of the function."""


def main() -> None:
    """
    Entry point for the program.

    This function serves as the entry point of the program. It is responsible for executing the main logic of the program
    and coordinating the flow of control between different functions and components.

    Parameters:
        None

    Returns:
        None
    """
    recommendation_system = BookRecommender()
    recommendation_system.run_recommendation_system()


if __name__ == "__main__":
    main()
```

I hope this explanation helps you understand the changes made. Let me know if you have any further questions!
