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

# Question 2: Sleep, mood, and activity

mood_mapping = {'Tired': 1, 'Neutral': 2, 'Happy': 3}
try:
    df['mood_numerical'] = df['mood'].map(mood_mapping)
except KeyError:
    print("Error: 'mood' column not found or contains unexpected values.")
    exit()
df.dropna(subset=['mood_numerical'], inplace=True)

for activity_type in ['active_minutes', 'steps']:
    # Create subplots for each mood
    unique_moods = sorted(df['mood_numerical'].unique()) #Sort the moods for consistent plotting
    num_moods = len(unique_moods)

    fig, axes = plt.subplots(1, num_moods, figsize=(5*num_moods, 5), squeeze=False)

    for i, mood_val in enumerate(unique_moods):
        df_mood = df[df['mood_numerical'] == mood_val]

        #Scatter plot
        axes[0, i].scatter(df_mood['sleep_hours'], df_mood[activity_type])
        
        #Calculate and plot trendline
        z = np.polyfit(df_mood['sleep_hours'], df_mood[activity_type], 1)
        p = np.poly1d(z)
        axes[0, i].plot(df_mood['sleep_hours'],p(df_mood['sleep_hours']),"r--")

        axes[0, i].set_title(f"Mood: {mood_val}")
        axes[0, i].set_xlabel('Sleep Hours')
        axes[0, i].set_ylabel(activity_type)

    fig.suptitle(f"Sleep vs. {activity_type} (by Mood)", fontsize=16) #Add a super title for the entire figure
    plt.tight_layout()
    plt.subplots_adjust(top=0.85) #Adjust the top margin to prevent overlap with the suptitle
    plt.show()

    #Overall scatter plot
    plt.scatter(df['sleep_hours'], df[activity_type], c=df['mood_numerical'])
    plt.title(f"Overall Sleep vs. {activity_type} (by Mood)")
    plt.xlabel('Sleep Hours')
    plt.ylabel(activity_type)
    plt.colorbar(label="Mood")
    plt.show()