import os
import requests
from django.core.management.base import BaseCommand

from travel.models import District


class Command(BaseCommand):
    help = "Load districts data into db"

    def handle(self, *args, **kwargs):
        if districts_data := self.fetch_district_data():
            for district in districts_data.get("districts"):
                if District.objects.filter(name=district.get("name")).exists():
                    continue

                District.objects.create(
                    division_id=district.get("division_id"),
                    name=district.get("name"),
                    bn_name=district.get("bn_name"),
                    lat=float(district.get("lat")),
                    long=float(district.get("long")),
                )

            self.stdout.write(self.style.SUCCESS("Successfully synced districts data."))
        else:
            self.stdout.write(self.style.WARNING("No district data found to sync."))

    def fetch_district_data(self):
        result = dict()

        try:
            response = requests.get(os.getenv("DISTRICT_INFO_URL"))
            result = response.json()
        except requests.RequestException as error:
            self.stderr.write(
                self.style.ERROR(f"Failed to fetch district data: {error}")
            )
        except Exception as error:
            self.stderr.write(
                self.style.ERROR(f"Failed to fetch district data: {error}")
            )

        return result
