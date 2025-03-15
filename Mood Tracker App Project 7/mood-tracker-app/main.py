import streamlit as st  # For creating web interface
import pandas as pd  # For data manipulation
import datetime  # For handling dates
import csv  # For reading and writing CSV file
import os  # For file operations

# Define the file name for storing mood data
MOOD_FILE = "mood_log.csv"

# Function to read mood data from the CSV file
def load_mood_data():
    # Check if the file exists
    if not os.path.exists(MOOD_FILE):
        # If no file, create empty DataFrame with columns
        return pd.DataFrame(columns=["Date", "Mood"])
    
    # Read CSV file with proper handling
    data = pd.read_csv(MOOD_FILE, names=["Date", "Mood"], header=0)
    
    # Strip column names to remove unwanted spaces
    data.columns = data.columns.str.strip()
    
    return data

# Function to add new mood entry to CSV file
def save_mood_data(date, mood):
    # Open file in append mode
    with open(MOOD_FILE, "a", newline="") as file:
        # Create CSV writer
        writer = csv.writer(file)
        # Add new mood entry
        writer.writerow([date, mood])

# Streamlit app title with styling
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>Mood Tracker</h1>
    """, unsafe_allow_html=True)

# Get today's date
today = datetime.date.today()

# Create subheader for mood input with custom style
st.markdown("""
    <h3 style='color: #FF5733;'>How are you feeling today?</h3>
    """, unsafe_allow_html=True)

# Create dropdown for mood selection with a styled UI
mood = st.selectbox("Select your mood", ["😊 Happy", "😢 Sad", "😡 Angry", "😐 Neutral"], index=0)

# Create button to save mood with a custom style
if st.button("💾 Log Mood", key="log_mood", help="Click to save your mood"):
    # Save mood when button is clicked
    save_mood_data(today, mood)
    # Show success message with emoji
    st.success("✅ Mood Logged Successfully!")

# Load existing mood data
data = load_mood_data()

# If there is data to display
if not data.empty:
    # Convert date strings to datetime objects safely
    try:
        data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
    except KeyError:
        st.error("❌ Error: 'Date' column not found in data!")
    
    # Drop any rows where date conversion failed
    data = data.dropna(subset=["Date"])
    
    # Count frequency of each mood
    mood_counts = data.groupby("Mood").count()["Date"]
    
    # Display bar chart of mood frequencies with a stylish section
    st.markdown("""
        <h3 style='color: #3498DB;'>Mood Trends Over Time</h3>
        """, unsafe_allow_html=True)
    st.bar_chart(mood_counts, use_container_width=True)
else:
    st.warning("⚠️ No mood data available yet. Please log your mood first.")

# Footer with custom styling
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <p>Built with ❤️ by <strong>Saba Muhammad Riaz</strong></p>
    </div>
    """, unsafe_allow_html=True)

    
