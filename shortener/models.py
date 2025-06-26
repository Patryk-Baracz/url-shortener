import random, string
from django.db import models

# Create your models here.

class ShortenedURL(models.Model):
    original_url = models.URLField(unique=True)
    shortened_url = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shortened_url
    
    def save(self, *args, **kwargs):
        if not self.shortened_url:
            self.generate_shortened_url()
        super().save(*args, **kwargs)

    def generate_shortened_url(self, length: int = 6) -> None:
        """Generate a unique shortened URL and assign it to the instance."""
        while True:
            code = self.generate_random_code(length)
            if not self.is_code_taken(code):
                self.shortened_url = code
                break

    @classmethod
    def is_code_taken(cls, code: str) -> bool:
        return cls.objects.filter(shortened_url=code).exists()

    @staticmethod
    def generate_random_code(length: int = 6) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
