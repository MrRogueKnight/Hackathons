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

for col in ['sleep_hours', 'active_minutes', 'steps']:
    try:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    except KeyError:
        print(f"Error: Column '{col}' not found.")
        exit()
df.dropna(inplace=True)

# Question 3: Location, mood, and weather

mood_mapping = {'Tired': 1, 'Neutral': 2, 'Happy': 3}
try:
    df['mood_numerical'] = df['mood'].map(mood_mapping)
except KeyError:
    print("Error: 'mood' column not found or contains unexpected values.")
    exit()
df.dropna(subset=['mood_numerical'], inplace=True)

# Create cross-tabulations and visualize with stacked bar charts
unique_weather = df['weather_conditions'].unique()
unique_locations = df['location'].unique()

for weather in unique_weather:
    df_weather = df[df['weather_conditions'] == weather]
    
    fig, axes = plt.subplots(1, len(unique_locations), figsize=(5*len(unique_locations), 5), squeeze=False)
    fig.suptitle(f"Mood Distribution by Location (Weather: {weather})", fontsize=16)
    
    for i, location in enumerate(unique_locations):
        df_location_weather = df_weather[df_weather['location'] == location]
        if not df_location_weather.empty:
            mood_counts = df_location_weather['mood'].value_counts(normalize=True) #Normalize to get proportions
            mood_labels = mood_counts.index.tolist()
            mood_values = mood_counts.values.tolist()
            
            axes[0,i].bar(mood_labels, mood_values)
            axes[0,i].set_title(f"Location: {location}")
            axes[0,i].set_ylabel("Proportion of Mood")
            axes[0,i].set_xlabel("Mood")
        else:
            axes[0,i].axis("off")
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()

#Overall plot
fig, axes = plt.subplots(1, len(unique_locations), figsize=(5*len(unique_locations), 5), squeeze=False)
fig.suptitle(f"Overall Mood Distribution by Location", fontsize=16)
for i, location in enumerate(unique_locations):
    df_location = df[df['location'] == location]
    if not df_location.empty:
        mood_counts = df_location['mood'].value_counts(normalize=True) #Normalize to get proportions
        mood_labels = mood_counts.index.tolist()
        mood_values = mood_counts.values.tolist()
        
        axes[0,i].bar(mood_labels, mood_values)
        axes[0,i].set_title(f"Location: {location}")
        axes[0,i].set_ylabel("Proportion of Mood")
        axes[0,i].set_xlabel("Mood")
    else:
        axes[0,i].axis("off")
plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.show()