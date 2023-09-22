import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional


class Book:
    def __init__(self, title: str, author: str, genre: str, rating: float, reviews: int, url: str, summary: str) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.reviews = reviews
        self.url = url
        self.summary = summary

    def get_summary(self) -> str:
        return self.summary

    def __str__(self) -> str:
        return f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}\nRating: {self.rating}\nReviews: {self.reviews}\nSummary: {self.summary[:100]}...\nURL: {self.url}\n"


class BookRecommendationSystem:
    def __init__(self) -> None:
        self.books: List[Book] = []

    def scrape_book_data(self) -> None:
        url = "https://www.goodreads.com/genre/show/19-science-fiction"
        response = requests.get(url)
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
            if summary_element:
                summary = summary_element.text.strip()
            else:
                summary = "Summary not available"

            book = Book(title, author, genre, rating, reviews, url, summary)
            self.books.append(book)

    def get_book_recommendations(self, user_input: str) -> List[Book]:
        user_vector = self._preprocess_input(user_input)
        if not user_vector:
            return []

        similarity_scores = self._calculate_similarity(user_vector)
        sorted_books = sorted(
            zip(self.books, similarity_scores), key=lambda x: x[1], reverse=True)
        return [book for book, _ in sorted_books[:5]]

    def _preprocess_input(self, user_input: str) -> Optional[List[float]]:
        documents = [book.get_summary() for book in self.books]
        if not documents:
            return None

        documents.append(user_input)
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(documents)

        user_vector = matrix[-1].toarray()[0].tolist()
        return user_vector

    def _calculate_similarity(self, user_vector: List[float]) -> List[float]:
        if not self.books:
            return []

        book_vectors = [vector.tolist() for book in self.books]
        similarity_scores = cosine_similarity([user_vector], book_vectors)[0]
        return similarity_scores

    def print_recommendations(self, recommendations: List[Book]):
        print("Personalized Book Recommendations:")
        if recommendations:
            for i, book in enumerate(recommendations, start=1):
                print(f"{i}.")
                print(book)
        else:
            print("No book recommendations found.")

    def run_recommendation_system(self):
        self.scrape_book_data()

        while True:
            user_input = input("Enter a genre you like (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break
            recommendations = self.get_book_recommendations(user_input)
            self.print_recommendations(recommendations)


if __name__ == "__main__":
    recommendation_system = BookRecommendationSystem()
    recommendation_system.run_recommendation_system()
