"""
Django management command for importing tracks from JSON file.
"""

import json
import os
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from player.models import Track, Artist, Genre


class Command(BaseCommand):
    """Command to import tracks from JSON file."""

    help = "Импорт треков из JSON-файла"

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str, help="Путь к JSON-файлу с треками")

    def handle(self, *args, **kwargs):
        json_path = kwargs["json_path"]

        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f"Файл {json_path} не найден"))  # pylint: disable=no-member
            return

        with open(json_path, "r", encoding="utf-8") as file:
            tracks_data = json.load(file)

        for track_data in tracks_data:
            try:
                main_author = Artist.objects.get(id=track_data["main_author"])
                genre = Genre.objects.get(id=track_data["genre"])

                track = Track(
                    name=track_data["name"],
                    main_author=main_author,
                    genre=genre,
                    publication_time=make_aware(
                        datetime.fromisoformat(track_data["publication_time"])
                    )
                )

                if track_data.get("logo"):
                    with open(track_data["logo"], "rb") as img_file:
                        track.logo.save(  # pylint: disable=no-member
                            os.path.basename(track_data["logo"]),
                            ContentFile(img_file.read()),
                            save=False
                        )

                if track_data.get("mp3"):
                    with open(track_data["mp3"], "rb") as mp3_file:
                        track.mp3.save(  # pylint: disable=no-member
                            os.path.basename(track_data["mp3"]),
                            ContentFile(mp3_file.read()),
                            save=False
                        )

                track.save()

                if track_data.get("featured_authors"):
                    featured_authors = Artist.objects.filter(
                        id__in=track_data["featured_authors"]
                    )
                    track.featured_authors.set(featured_authors)  # pylint: disable=no-member

                self.stdout.write(  # pylint: disable=no-member
                    self.style.SUCCESS(f"Трек '{track.name}' успешно добавлен") # pylint: disable=E1101
                )
            except Exception as exc:  # pylint: disable=broad-except
                self.stderr.write(  # pylint: disable=no-member
                    self.style.ERROR(
                        f"Ошибка при обработке трека '{track_data['name']}': {exc}"
                    )
                )
