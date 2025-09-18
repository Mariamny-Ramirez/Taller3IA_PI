import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Verifica que los embeddings estén almacenados correctamente en la base de datos"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        self.stdout.write(self.style.SUCCESS(f"Se encontraron {movies.count()} películas en la base de datos"))

        for i, movie in enumerate(movies):
            try:
                embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
                self.stdout.write(f"{movie.title}: {embedding_vector[:5]} ...")  # solo 5 valores
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error con {movie.title}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("✅ Verificación completada"))
