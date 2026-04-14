from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class Language(models.Model):
      name = models.CharField(max_length=100)
      photo = models.ImageField(upload_to = 'photos', blank=True, null=True)
      slug = models.SlugField(max_length=100, unique=True)

      def __str__(self):
          return f"Назва: {self.name}"

      def get_absolute_url(self):
          return reverse('category', kwargs={'show_cat': self.slug})


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.CharField(max_length=120)
    lang = models.ForeignKey('Language', on_delete=models.CASCADE)
    file = models.FileField(upload_to = 'files')

    def __str__(self):
        return f"Назва: {self.name}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'show_more': self.slug})

class TechnologyDetail(models.Model):
    topic = models.CharField(max_length=100)
    photo = models.ImageField(upload_to = 'photos')
    description = models.CharField()
    tech = models.ForeignKey('Technology', on_delete=models.CASCADE)

class Saved(models.Model):
      email = models.EmailField(max_length=100)
      detail = models.ForeignKey('Technology', on_delete=models.CASCADE)

      def __str__(self):
          return self.email

      def get_absolute_url(self):
          return reverse('detail', kwargs={'show_more': self.detail.slug})


