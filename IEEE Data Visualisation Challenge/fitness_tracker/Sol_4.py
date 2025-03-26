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

for col in ['sleep_hours', 'active_minutes', 'steps', 'calories_burned', 'heart_rate_avg']:
    try:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    except KeyError:
        print(f"Error: Column '{col}' not found.")
        exit()
df.dropna(inplace=True)

# Question 4: Optimal steps/minutes for calorie burn (by workout type)

MAX_HEART_RATE = 170  # Define maximum heart rate

for workout in df['workout_type'].unique():
    df_workout = df[df['workout_type'] == workout]

    for activity_type in ['active_minutes', 'steps']:
        plt.figure(figsize=(10, 6))  # Create a new figure for each plot

        # Filter data based on MAX_HEART_RATE
        df_filtered = df_workout[df_workout['heart_rate_avg'] <= MAX_HEART_RATE]

        if df_filtered.empty:
            print(f"No data found for {workout} with heart rate below {MAX_HEART_RATE}")
            continue

        # Scatter Plot
        plt.scatter(df_filtered[activity_type], df_filtered['calories_burned'], label='Calories Burned', marker='o')
        plt.scatter(df_filtered[activity_type], df_filtered['heart_rate_avg'], label='Heart Rate', marker='x')

        # Calculate and plot trendline for Calories Burned
        z = np.polyfit(df_filtered[activity_type], df_filtered['calories_burned'], 1)
        p = np.poly1d(z)
        plt.plot(df_filtered[activity_type], p(df_filtered[activity_type]), "b--", label="Calories Trend")

        plt.axhline(y=MAX_HEART_RATE, color='r', linestyle='--', label=f'Max Heart Rate ({MAX_HEART_RATE})')

        plt.title(f'{activity_type} vs. Calories/Heart Rate ({workout})')
        plt.xlabel(activity_type)
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True) #Add a grid for better readability
        plt.show()

        #Optimal range calculation
        bins = np.linspace(df_filtered[activity_type].min(), df_filtered[activity_type].max(), 11) #Create 10 bins
        df_filtered['bins'] = pd.cut(df_filtered[activity_type], bins=bins, include_lowest=True)
        optimal_range = df_filtered.groupby('bins')['calories_burned'].mean()
        if not optimal_range.empty:
            best_bin = optimal_range.idxmax()
            print(f"Optimal {activity_type} range for {workout} is {best_bin} to maximize calorie burn without exceeding {MAX_HEART_RATE} heart rate")
        else:
            print(f"No suitable {activity_type} range found for {workout} within the heart rate limit")