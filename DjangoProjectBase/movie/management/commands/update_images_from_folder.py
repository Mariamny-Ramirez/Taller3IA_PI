import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie


def normalize(text: str) -> str:
    """
    Normaliza nombres para que coincidan entre BD y archivos:
    - minúsculas
    - quita caracteres inválidos (: ? / \ etc.)
    - elimina dobles espacios
    """
    text = text.lower()
    text = re.sub(r"[\\/*?\"'<>:|]", "", text)  # quitar caracteres ilegales
    text = re.sub(r"\s+", " ", text)  # reemplazar múltiples espacios por 1
    return text.strip()


class Command(BaseCommand):
    help = "Actualiza las imágenes de películas desde la carpeta media/movie/images/"

    def handle(self, *args, **kwargs):
        images_path = os.path.join(settings.MEDIA_ROOT, "movie", "images")
        if not os.path.exists(images_path):
            self.stdout.write(self.style.ERROR(f"❌ Carpeta no encontrada: {images_path}"))
            return

        # Diccionario: {nombre_normalizado: archivo_real}
        image_files = {
            normalize(f.replace("m_", "").replace(".png", "")): f
            for f in os.listdir(images_path)
            if f.endswith(".png")
        }

        movies = Movie.objects.all()
        self.stdout.write(f"📽️ Se encontraron {movies.count()} películas en la base de datos")

        updated = 0
        for movie in movies:
            normalized_title = normalize(movie.title)

            if normalized_title in image_files:
                image_file = image_files[normalized_title]
                movie.image = f"movie/images/{image_file}"
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Imagen asignada: {movie.title} → {image_file}"))
                updated += 1
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ No se encontró imagen para: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"🎉 Proceso terminado. {updated} películas actualizadas."))