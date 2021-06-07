from django.db import models


# Create your models here.


class ImageEntry(models.Model):
    nid = models.TextField()
    path = models.TextField()
    # store list in str format
    pos_labels = models.TextField()
    neg_labels = models.TextField()
    main_color = models.TextField()
    size_choices = [('Large', '大'),
                    ('Medium', '中'),
                    ('Small', '小')]
    size = models.CharField(max_length=20, choices=size_choices, default='Small')


class ImageLabel(models.Model):
    name = models.TextField()
    embed = models.TextField()
    invert_idx = models.TextField()


class WordEmbed(models.Model):
    word = models.TextField()
    embed = models.TextField()
