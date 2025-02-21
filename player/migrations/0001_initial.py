from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('logo', models.ImageField(null=True, upload_to='media/artists')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('sub_count', models.IntegerField(default=0)),
            ],
        ),
    ]
