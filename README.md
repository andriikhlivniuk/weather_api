## Setup and Installation

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```
3. Run the script:
```bash
python main.py
```
4. Result will be written into `weather_data_{timestamp}.csv` file
5. Data visualisation into `weather_plot_{timestamp}.png` file 

## Description

This Python program fetches real-time weather data from the Open-Meteo API for multiple cities worldwide. It retrieves current temperature, wind speed, and humidity data, processes it into a pandas DataFrame with additional unit conversions (Celsius to Fahrenheit, meters/second to mph), and generates comprehensive visualizations using matplotlib and seaborn. The program outputs both a CSV file containing the detailed weather data and a PNG file with two plots: a temperature comparison bar chart and a grouped bar chart showing humidity and wind speed relationships across cities. The results are automatically timestamped and saved locally, making it easy to track weather patterns over time.
