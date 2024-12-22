import requests
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

@dataclass
class WeatherData:
    city: str
    temperature: float
    wind_speed: float
    humidity: float
    timestamp: datetime

    def to_dict(self) -> Dict:
        """Convert WeatherData to dictionary for DataFrame creation"""
        return {
            'city': self.city,
            'temperature_c': self.temperature,
            'temperature_f': (self.temperature * 9/5) + 32,
            'wind_speed_kmh': self.wind_speed,
            'wind_speed_mph': self.wind_speed * 0.621371,
            'humidity': self.humidity,
            'timestamp': self.timestamp
        }

def get_coordinates(city: str) -> tuple[float, float]:
    """Get latitude and longitude for a given city using Open-Meteo Geocoding API"""
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(geocoding_url)
    data = response.json()
    
    if not data.get("results"):
        raise ValueError(f"Could not find coordinates for {city}")
    
    result = data["results"][0]
    return result["latitude"], result["longitude"]

def get_weather(city: str) -> WeatherData:
    """Fetch current weather data for a given city"""
    lat, lon = get_coordinates(city)
    
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    
    response = requests.get(weather_url)
    data = response.json()
    current = data["current"]
    
    return WeatherData(
        city=city,
        temperature=current["temperature_2m"],
        wind_speed=current["wind_speed_10m"],
        humidity=current["relative_humidity_2m"],
        timestamp=datetime.fromisoformat(current["time"])
    )

def get_weather_multiple_cities(cities: List[str]) -> List[WeatherData]:
    """Fetch weather data for multiple cities"""
    return [get_weather(city) for city in cities]

def process_weather_data(weather_data: List[WeatherData]) -> pd.DataFrame:
    """Process weather data and create a DataFrame with additional calculations"""
    # Convert list of WeatherData objects to list of dictionaries
    data_dicts = [data.to_dict() for data in weather_data]
    
    # Create DataFrame
    df = pd.DataFrame(data_dicts)
    
    # Sort cities by temperature (descending)
    df_by_temp = df.sort_values('temperature_c', ascending=False)
    
    # Sort cities by humidity (ascending)
    df_by_humidity = df.sort_values('humidity')
    
    print("\nCities Ranked by Temperature (Hottest to Coldest):")
    print(df_by_temp[['city', 'temperature_c', 'temperature_f']])
    
    print("\nCities Ranked by Humidity (Driest to Most Humid):")
    print(df_by_humidity[['city', 'humidity']])
    
    # Calculate summary statistics
    print("\nSummary Statistics:")
    print(df[['temperature_c', 'wind_speed_kmh', 'humidity']].describe())
    
    return df

def main():
    cities = ["London", "Paris", "New York", "Tokyo", "Sydney"]
    
    try:
        weather_data = get_weather_multiple_cities(cities)
        
        # Create and process DataFrame
        df = process_weather_data(weather_data)
        
        # Example of filtering: Cities with temperature above 10°C
        warm_cities = df[df['temperature_c'] > 10]
        if not warm_cities.empty:
            print("\nWarm Cities (>10°C):")
            print(warm_cities[['city', 'temperature_c', 'temperature_f']])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
