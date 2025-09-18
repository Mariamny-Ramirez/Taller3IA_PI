from django.db import models
import numpy as np

def get_default_array():
    # crea un array de tamaño 1536 (dimensión de text-embedding-3-small)
    default_arr = np.random.rand(1536)
    return default_arr.astype(np.float32).tobytes()

class Movie(models.Model): 
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)  # lo ampliamos un poco
    image = models.ImageField(upload_to='movie/images/', default='movie/images/default.jpg')
    url = models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)
    emb = models.BinaryField(default=get_default_array)  # nuevo campo para embeddings

    def _str_(self): 
        return self.title