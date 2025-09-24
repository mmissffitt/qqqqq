from django.db import models

class Author(models.Model):
    name = models.CharField(verbose_name="Имя автора", max_length=20)
    surname = models.CharField("Фамилия", max_length=25)
    birthday = models.DateField("Дата рождения")
    bio = models.TextField("Биография")

class Publisher(models.Model):
    name = models.CharField("Название", unique=True, blank=True)

class Book(models.Model):
    title = models.CharField("Название", max_length=50)
    id_publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    id_author = models.ManyToManyField(Author)

