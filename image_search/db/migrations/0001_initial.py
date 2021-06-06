# Generated by Django 3.2.4 on 2021-06-06 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nid', models.TextField()),
                ('path', models.TextField()),
                ('pos_labels', models.TextField()),
                ('neg_labels', models.TextField()),
                ('main_colors', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ImageLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nid', models.TextField()),
                ('name', models.TextField()),
                ('embed', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WordEmbed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('embed', models.TextField()),
            ],
        ),
    ]
