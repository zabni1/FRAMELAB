from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class LanguageDetail(models.Model):
      name = models.CharField(max_length=100)
      description = models.CharField(max_length=100)
      photo = models.ImageField(upload_to = 'photos')
      slug = models.SlugField(max_length=100, unique=True)
      lang = models.ForeignKey('Language', on_delete=models.CASCADE)
      cat = models.ForeignKey('LanguageDetailCategory', on_delete=models.CASCADE)

      def __str__(self):
          return f"Назва: {self.name}"

      def get_absolute_url(self):
          return reverse('detail', kwargs={'show_more': self.slug})

class Language(models.Model):
      name = models.CharField(max_length=100)
      photo = models.ImageField(upload_to = 'photos')
      slug = models.SlugField(max_length=100, unique=True)

      def __str__(self):
          return f"Назва: {self.name}"

      def get_absolute_url(self):
          return reverse('category', kwargs={'show_cat': self.slug})

class LanguageDetailCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f"Назва: {self.name}"

class Saved(models.Model):
      email = models.EmailField(max_length=100)
      detail = models.ForeignKey('LanguageDetail', on_delete=models.CASCADE)

      def __str__(self):
          return self.email

      def get_absolute_url(self):
          return reverse('detail', kwargs={'show_more': self.detail.slug})


