import json
import os
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime
from player.models import Track, Artist, Genre  # Укажите корректный путь к моделям

class Command(BaseCommand):
    help = "Импорт треков из JSON-файла"

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str, help="Путь к JSON-файлу с треками")

    def handle(self, *args, **kwargs):
        json_path = kwargs["json_path"]

        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f"Файл {json_path} не найден"))
            return

        with open(json_path, "r", encoding="utf-8") as file:
            tracks_data = json.load(file)

        for track_data in tracks_data:
            try:
                # Проверяем, существует ли основной автор
                main_author = Artist.objects.get(id=track_data["main_author"])

                # Проверяем, существует ли жанр
                genre = Genre.objects.get(id=track_data["genre"])

                # Создаём экземпляр Track без сохранения
                track = Track(
                    name=track_data["name"],
                    main_author=main_author,
                    genre=genre,
                    publication_time=make_aware(datetime.fromisoformat(track_data["publication_time"]))
                )

                # Загружаем логотип, если указан
                if "logo" in track_data and track_data["logo"]:
                    with open(track_data["logo"], "rb") as img_file:
                        track.logo.save(os.path.basename(track_data["logo"]), ContentFile(img_file.read()), save=False)

                # Загружаем MP3, если указан
                if "mp3" in track_data and track_data["mp3"]:
                    with open(track_data["mp3"], "rb") as mp3_file:
                        track.mp3.save(os.path.basename(track_data["mp3"]), ContentFile(mp3_file.read()), save=False)

                # Сохраняем объект
                track.save()

                # Добавляем приглашённых авторов
                if "featured_authors" in track_data:
                    featured_authors = Artist.objects.filter(id__in=track_data["featured_authors"])
                    track.featured_authors.set(featured_authors)

                self.stdout.write(self.style.SUCCESS(f"Трек '{track.name}' успешно добавлен"))
            except Artist.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Ошибка: Автор с ID {track_data['main_author']} не найден"))
            except Genre.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Ошибка: Жанр с ID {track_data['genre']} не найден"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Ошибка при обработке трека '{track_data['name']}': {e}"))
