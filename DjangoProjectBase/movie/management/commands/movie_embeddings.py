import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from dotenv import load_dotenv
from openai import OpenAI

class Command(BaseCommand):
    help = "Generate and store embeddings for all movies"

    def handle(self, *args, **kwargs):
        # 1. Cargar API Key
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # 2. Recuperar todas las películas
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            try:
                # 3. Generar embedding usando la descripción
                response = client.embeddings.create(
                    input=movie.description,
                    model="text-embedding-3-small"
                )
                emb_array = np.array(response.data[0].embedding, dtype=np.float32)

                # 4. Guardar embedding como binario
                movie.emb = emb_array.tobytes()
                movie.save()

                self.stdout.write(self.style.SUCCESS(f"✅ Embedding stored for: {movie.title}"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ Failed to embed {movie.title}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("✨ Finished generating embeddings for all movies"))
