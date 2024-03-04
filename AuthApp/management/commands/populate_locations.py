from django.core.management.base import BaseCommand
import requests
from AuthApp.models import Country, City

class Command(BaseCommand):
    help = 'Populates the database with countries and cities from an API'

    def handle(self, *args, **options):
        # Populate countries
        countries_response = requests.get('https://restcountries.com/v3.1/all')
        if countries_response.status_code == 200:
            for country_data in countries_response.json():
                country, created = Country.objects.get_or_create(name=country_data['name']['common'])
                self.stdout.write(self.style.SUCCESS(f'{"Added" if created else "Exists"} country {country.name}'))

                # Fetch cities for the country from GeoNames
                cities_response = requests.get(
                    f'http://api.geonames.org/searchJSON?country={country_data["cca2"]}&maxRows=10&username=YOUR_GEONAMES_USERNAME&cities=cities15000'
                )
                if cities_response.status_code == 200:
                    cities_data = cities_response.json()
                    for city_info in cities_data['geonames']:
                        city, created = City.objects.get_or_create(
                            name=city_info['name'],
                            country=country
                        )
                        msg = f'Added city {city.name} in {country.name}' if created else f'Exists city {city.name} in {country.name}'
                        self.stdout.write(self.style.SUCCESS(msg))
