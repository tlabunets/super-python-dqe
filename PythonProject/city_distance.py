import sqlite3
import math

DB_NAME = "cities.db"

class CityDatabase:
    def __init__(self, db_path=DB_NAME):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Creates the city table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                name TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        ''')
        self.conn.commit()

    def get_coordinates(self, city_name):
        """Returns (lat, lon) if city is found, otherwise None."""
        self.cursor.execute("SELECT latitude, longitude FROM cities WHERE name = ?", (city_name.lower(),))
        result = self.cursor.fetchone()
        return result if result else None

    def save_coordinates(self, city_name, latitude, longitude):
        """Saves new city coordinates to DB."""
        self.cursor.execute(
            "INSERT OR REPLACE INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
            (city_name.lower(), latitude, longitude)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()


def haversine_distance(lat1, lon1, lat2, lon2):
    """Returns distance in km between two geographic coordinates using the Haversine formula."""
    R = 6371  # Earth radius in km

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)


def get_or_prompt_coordinates(city_name, db):
    """Checks DB for coordinates, prompts user if missing."""
    coords = db.get_coordinates(city_name)
    if coords:
        return coords
    else:
        print(f"Coordinates for '{city_name}' not found.")
        lat = float(input(f"Enter latitude for {city_name}: "))
        lon = float(input(f"Enter longitude for {city_name}: "))
        db.save_coordinates(city_name, lat, lon)
        return lat, lon


def main():
    print("📍 City Distance Calculator")

    city1 = input("Enter first city name: ").strip()
    city2 = input("Enter second city name: ").strip()

    db = CityDatabase()

    lat1, lon1 = get_or_prompt_coordinates(city1, db)
    lat2, lon2 = get_or_prompt_coordinates(city2, db)

    distance = haversine_distance(lat1, lon1, lat2, lon2)
    print(f"\nDistance between {city1} and {city2}: {distance} km")

    db.close()


if __name__ == "__main__":
    main()