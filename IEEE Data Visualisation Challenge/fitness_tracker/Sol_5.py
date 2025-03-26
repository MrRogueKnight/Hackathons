import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data loading and cleaning (as before)
try:
    df = pd.read_csv('fitness_tracker_dataset.csv')
except FileNotFoundError:
    print("Error: 'fitness_tracker_dataset.csv' not found.")
    exit()

try:
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
except (ValueError, KeyError):
    print("Error with 'date' column. Check format or existence.")
    exit()

for col in ['sleep_hours', 'active_minutes', 'steps', 'calories_burned', 'heart_rate_avg','distance_km']:
    try:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    except KeyError:
        print(f"Error: Column '{col}' not found.")
        exit()
df.dropna(inplace=True)

# Question 5: Weather influence on workout/location, and subsequent effects

mood_mapping = {'Tired': 1, 'Neutral': 2, 'Happy': 3}
try:
    df['mood_numerical'] = df['mood'].map(mood_mapping)
except KeyError:
    print("Error: 'mood' column not found or contains unexpected values.")
    exit()
df.dropna(subset=['mood_numerical'], inplace=True)
df['mood'] = df['mood'].astype('category')
df['workout_type'] = df['workout_type'].astype('category')
df['location'] = df['location'].astype('category')
df['weather_conditions'] = df['weather_conditions'].astype('category')

unique_weather = df['weather_conditions'].unique()

for weather in unique_weather:
    df_weather = df[df['weather_conditions'] == weather]

    # Workout Type Distribution by Weather
    workout_counts = df_weather['workout_type'].value_counts(normalize=True)
    plt.figure()
    workout_counts.plot(kind='bar', title=f"Workout Type Distribution ({weather})")
    plt.ylabel("Proportion")
    plt.show()

    # Location Distribution by Weather
    location_counts = df_weather['location'].value_counts(normalize=True)
    plt.figure()
    location_counts.plot(kind='bar', title=f"Location Distribution ({weather})")
    plt.ylabel("Proportion")
    plt.show()

    unique_workout = df['workout_type'].unique()
    for workout in unique_workout:
      df_workout_weather = df_weather[df_weather['workout_type'] == workout]
      if not df_workout_weather.empty:
        # Mood Distribution by Workout and Weather
        mood_counts = df_workout_weather['mood'].value_counts(normalize=True)
        plt.figure()
        mood_counts.plot(kind='pie', title=f"Mood Distribution ({workout}, {weather})", autopct='%1.1f%%')
        plt.ylabel("")
        plt.show()

        # Metrics Distribution by Workout and Weather
        metrics = df_workout_weather[['calories_burned', 'heart_rate_avg','active_minutes','steps','distance_km']].mean()
        plt.figure()
        metrics.plot(kind='bar', title=f"Metrics Distribution ({workout}, {weather})")
        plt.ylabel("Value")
        plt.show()
      else:
        print(f"No data found for {workout} in {weather}")

    unique_location = df['location'].unique()
    for location in unique_location:
      df_location_weather = df_weather[df_weather['location'] == location]
      if not df_location_weather.empty:
        # Mood Distribution by Location and Weather
        mood_counts = df_location_weather['mood'].value_counts(normalize=True)
        plt.figure()
        mood_counts.plot(kind='pie', title=f"Mood Distribution ({location}, {weather})", autopct='%1.1f%%')
        plt.ylabel("")
        plt.show()

        # Metrics Distribution by Location and Weather
        metrics = df_location_weather[['calories_burned', 'heart_rate_avg','active_minutes','steps','distance_km']].mean()
        plt.figure()
        metrics.plot(kind='bar', title=f"Metrics Distribution ({location}, {weather})")
        plt.ylabel("Value")
        plt.show()
      else:
        print(f"No data found for {location} in {weather}")