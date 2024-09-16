import csv
import os

class CountryInfo:
    def __init__(self, country, capital, continent, population, language):
        self.country = country
        self.capital = capital
        self.continent = continent
        self.population = population
        self.language = language

    def __str__(self):
        return f"Country: {self.country}, Capital: {self.capital}, Continent: {self.continent}, Population: {self.population}, Language: {self.language}"


class CountryDatabase:
    def __init__(self, csv_filename):
        self.countries = []
        self.load_data(csv_filename)
        if not os.path.exists(csv_filename):
            print(f"File '{csv_filename}' not found!")
            return
       

    def load_data(self, csv_filename):
        """Loads data from the CSV file and stores it in a list of CountryInfo objects."""
        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country_info = CountryInfo(
                    row['Country'],
                    row['Capital'],
                    row['Continent'],
                    int(row['Population']),
                    row['Language']
                )
                self.countries.append(country_info)
        # Sort the list of countries alphabetically for binary search
        self.countries.sort(key=lambda country: country.country)

    def binary_search(self, target_country):
        """Performs a binary search for the target country in the sorted list."""
        low = 0
        high = len(self.countries) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_country = self.countries[mid].country

            if mid_country.lower() == target_country.lower():
                return self.countries[mid]
            elif mid_country.lower() < target_country.lower():
                low = mid + 1
            else:
                high = mid - 1

        return None  # Country not found

    def search_country(self, country_name):
        """Searches for the country by name using binary search."""
        result = self.binary_search(country_name)
        if result:
            print(result)
        else:
            print(f"Country '{country_name}' not found in the database.")


 

# Usage Example
if __name__ == "__main__":
    # Create a CountryDatabase from a CSV file
    database = CountryDatabase('/Users/vincentdo/Downloads/countries1.csv')
    
    # Search for a country by name
    database.search_country('Colombia') 
