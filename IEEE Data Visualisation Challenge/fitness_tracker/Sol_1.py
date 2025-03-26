import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Question 1: Workout effects on calorie burn and heart rate (by weather and location)

# Create subplots for each combination of weather and location
unique_weather = df['weather_conditions'].unique()
unique_locations = df['location'].unique()

num_plots = len(unique_weather) * len(unique_locations)
if num_plots > 0:
    fig, axes = plt.subplots(len(unique_weather), len(unique_locations), figsize=(15, 5*len(unique_weather)), squeeze=False)
else:
    print("No unique weather and location found")
    exit()

plot_index = 0
for i, weather in enumerate(unique_weather):
    for j, location in enumerate(unique_locations):
        df_filtered = df[(df['weather_conditions'] == weather) & (df['location'] == location)]

        if not df_filtered.empty:
            df_grouped = df_filtered.groupby('workout_type')[['calories_burned', 'heart_rate_avg']].mean()
            
            # Plotting with Matplotlib
            x = np.arange(len(df_grouped))  # the label locations
            width = 0.35  # the width of the bars
            
            axes[i, j].bar(x - width/2, df_grouped['calories_burned'], width, label='Calories Burned')
            axes[i, j].bar(x + width/2, df_grouped['heart_rate_avg'], width, label='Heart Rate')
            
            axes[i, j].set_xticks(x)
            axes[i, j].set_xticklabels(df_grouped.index, rotation=45, ha='right')
            axes[i, j].set_ylabel('Value')
            axes[i, j].set_title(f"Workout Effects ({weather}, {location})")
            axes[i, j].legend()
        else:
            axes[i, j].axis('off') #Hide the plot if the data is empty

plt.tight_layout()
plt.show()

#Overall plot
df_grouped = df.groupby('workout_type')[['calories_burned', 'heart_rate_avg']].mean()

# Plotting with Matplotlib
x = np.arange(len(df_grouped))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
ax.bar(x - width/2, df_grouped['calories_burned'], width, label='Calories Burned')
ax.bar(x + width/2, df_grouped['heart_rate_avg'], width, label='Heart Rate')

ax.set_xticks(x)
ax.set_xticklabels(df_grouped.index, rotation=45, ha='right')
ax.set_ylabel('Value')
ax.set_title(f"Overall Workout Effects")
ax.legend()
plt.tight_layout()
plt.show()