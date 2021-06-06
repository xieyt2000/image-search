from django.db import models

# Create your models here.


class ImageEntry(models.Model):
    nid = models.TextField()
    path = models.TextField()
    # store list in str format
    pos_labels = models.TextField()
    neg_labels = models.TextField()
    main_colors = models.TextField()


class ImageLabel(models.Model):
    nid = models.TextField()
    name = models.TextField()
    embed = models.TextField()


class WordEmbed(models.Model):
    word = models.TextField()
    embed = models.TextField()
