import os
from datetime import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg


def upload_to_folder(instance, filename):
    today_date = datetime.today().date()
    return os.path.join(instance.genre, str(today_date), filename)


def upload_to_picture(instance, filename):
    today_date = datetime.today().date()
    return os.path.join(instance.language, str(today_date), filename)


class Channel(models.Model):
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=20)  # can make choice field
    picture = models.ImageField(upload_to=upload_to_picture, blank=True)
    sub_channel = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name="sub_channels")

    def __str__(self) -> str:
        return f'id: {self.id} title: {self.title} - lang: {self.language}'

    @property
    def average_rating(self):
        if hasattr(self, 'rating'):
            return getattr(self, "rating")
        if hasattr(self, 'sub_channels') and self.sub_channels:  # pylint: disable=E1101
            list_sub_channels = self.sub_channels.all()
            if list(list_sub_channels):
                channel_rating_list = []
                for sub in list_sub_channels:
                    if hasattr(sub, "average_rating"):
                        channel_rating_list.append(sub.average_rating["rating__avg"])
                sub_rating = sum(channel_rating_list) / len(channel_rating_list)
                contents_rating = self.contents.aggregate(Avg('rating'))
                if contents_rating["rating__avg"] and sub_rating:
                    self.rating = {"rating__avg": ((float(sub_rating) + float(contents_rating["rating__avg"])) / 2)}
                    return {"rating__avg": ((float(sub_rating) + float(contents_rating["rating__avg"])) / 2)}
                if sub_rating:
                    self.rating = {"rating__avg": sub_rating}
                    return {"rating__avg": sub_rating}
        self.rating = self.contents.aggregate(Avg('rating'))
        return self.contents.aggregate(Avg('rating'))


class Content(models.Model):
    FILE = 'file'
    VIDEO = 'video'
    TEXT = 'text'
    CONTENT_TYPES = [
        (FILE, 'File'),
        (VIDEO, 'Video'),
        (TEXT, 'Text')
    ]
    content_type = models.CharField(
        max_length=10, choices=CONTENT_TYPES, default=TEXT)
    url = models.FileField(upload_to=upload_to_folder)
    content_description = models.CharField(max_length=200)
    authors = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    rating_count = models.PositiveIntegerField(default=0, editable=False)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    channel = models.ForeignKey(
        Channel, on_delete=models.SET_NULL, blank=True, null=True, default=None, related_name="contents")

    def __str__(self) -> str:
        return f'{self.id} - {self.content_type} - {self.url}'

    @ classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)

        # save original values, when model is loaded from database,
        # in a separate attribute on the model
        instance._loaded_values = dict(zip(field_names, values))

        return instance

    def save(self, *args, **kwargs):
        if self.rating:
            self.rating_count += 1
            # if updating rating
            if hasattr(self, '_loaded_values'):
                rating = self.rating
                self.rating = (self._loaded_values['rating'] + rating) // self.rating_count
        return super(Content, self).save(*args, **kwargs)
