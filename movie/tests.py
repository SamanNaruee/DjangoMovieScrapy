from django.test import TestCase

from .models import Movie

class MovieModelTest(TestCase):
    def setUp(self):
        Movie.objects.create(title="The Matrix", year=1999, rating=8.7)
        Movie.objects.create(title="The Matrix Reloaded", year=2003, rating=7.2)
        Movie.objects.create(title="The Matrix Revolutions", year=2003, rating=6.7)
    
    def test_matrix_movie_creation(self):
        matrix = Movie.objects.get(title="The Matrix")
        self.assertEqual(matrix.title, "The Matrix")
        self.assertEqual(matrix.year, 1999)
        self.assertEqual(matrix.rating, 8.7)
        
    def test_matrix_reloaded_movie_creation(self):
        matrix_reloaded = Movie.objects.get(title="The Matrix Reloaded")
        self.assertEqual(matrix_reloaded.title, "The Matrix Reloaded")
        self.assertEqual(matrix_reloaded.year, 2003)
        self.assertEqual(matrix_reloaded.rating, 7.2)

    def test_matrix_revolutions_movie_creation(self):
        matrix_revolutions = Movie.objects.get(title="The Matrix Revolutions")
        self.assertEqual(matrix_revolutions.title, "The Matrix Revolutions")
        self.assertEqual(matrix_revolutions.year, 2003)
        self.assertEqual(matrix_revolutions.rating, 6.7)