import streamlit as st
import numpy as np
import pandas as pd
import time
import hashlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load user data from Excel
def load_users():
    try:
        return pd.read_excel("users.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Name", "Password"])

# Save user data to Excel
def save_user(username, name, password):
    users = load_users()
    if username in users["Username"].values:
        return False  # User already exists
    new_user = pd.DataFrame([[username, name, hash_password(password)]], columns=["Username", "Name", "Password"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_excel("users.xlsx", index=False)
    return True

# Authenticate user
def authenticate(username, password):
    users = load_users()
    user_row = users[users["Username"] == username]
    if not user_row.empty and user_row.iloc[0]["Password"] == hash_password(password):
        return True
    return False

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login & Signup Page
if not st.session_state.logged_in:
    st.title("Personal Fitness Tracker - Login")
    choice = st.radio("Select an option", ["Login", "Signup"])
    
    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    elif choice == "Signup":
        username = st.text_input("Username")
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Signup"):
            if password == confirm_password:
                if save_user(username, name, password):
                    st.success("Signup successful! Please login.")
                else:
                    st.error("Username already exists. Try another.")
            else:
                st.error("Passwords do not match.")
    
    st.stop()  
    
    # ---------------- UI DESIGN ----------------
st.set_page_config(page_title="Personal Fitness Tracker", layout="wide")  # MUST be the first Streamlit command
st.markdown("""
    <style>
        .big-font {font-size:70px !important; text-align: center; color: #008080; font-family: Bookman Old Style;}
        .small-font {font-size:24px !important; text-align: center; color: gray; font-family: Time Roman New;}
        .stButton>button { background-color: #4CAF50; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font"><b>Personal Fitness Tracker</b></p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">Track and predict calories burned based on your workout parameters.</p>', unsafe_allow_html=True)
st.write("---")
# Prevent access to main app before login

# Main Application (Existing Code Here)
st.title("Welcome to Personal Fitness Tracker")

# Yoga Poses Dataset
yoga_poses = {
    "Standing Poses (Balance & Strength)": [
        "Tadasana (Mountain Pose)",
        "Vrikshasana (Tree Pose)",
        "Utkatasana (Chair Pose)",
        "Garudasana (Eagle Pose)",
        "Virabhadrasana I (Warrior I)"
    ],
    "Forward Bends (Stretch & Release)": [
        "Uttanasana (Standing Forward Bend)",
        "Paschimottanasana (Seated Forward Bend)",
        "Janu Sirsasana (Head-to-Knee Forward Bend)",
        "Balasana (Child’s Pose)",
        "Ardha Uttanasana (Half Forward Bend)"
    ],
    "Backbends (Spine & Energy Boost)": [
        "Bhujangasana (Cobra Pose)",
        "Ustrasana (Camel Pose)",
        "Dhanurasana (Bow Pose)",
        "Matsyasana (Fish Pose)",
        "Setu Bandhasana (Bridge Pose)"
    ],
    "Twisting Poses (Detox & Core Strength)": [
        "Ardha Matsyendrasana (Half Lord of the Fishes Pose)",
        "Bharadvajasana (Sage Twist Pose)",
        "Parivrtta Utkatasana (Revolved Chair Pose)",
        "Marichyasana (Marichi’s Pose)",
        "Supine Spinal Twist (Supta Matsyendrasana)"
    ],
    "Hip Openers (Flexibility & Mobility)": [
        "Baddha Konasana (Butterfly Pose)",
        "Upavistha Konasana (Wide-Legged Forward Bend)",
        "Eka Pada Rajakapotasana (Pigeon Pose)",
        "Ananda Balasana (Happy Baby Pose)",
        "Gomukhasana (Cow Face Pose)"
    ],
    "Core Strengthening Poses": [
        "Navasana (Boat Pose)",
        "Phalakasana (Plank Pose)",
        "Paripurna Navasana (Full Boat Pose)",
        "Chaturanga Dandasana (Four-Limbed Staff Pose)",
        "Vasisthasana (Side Plank Pose)"
    ],
    "Arm Balancing Poses (Upper Body Strength)": [
        "Bakasana (Crow Pose)",
        "Eka Pada Koundinyasana (One-Legged Arm Balance)",
        "Tittibhasana (Firefly Pose)",
        "Astavakrasana (Eight-Angle Pose)",
        "Pincha Mayurasana (Forearm Stand)"
    ],
    "Inversions (Circulation & Focus)": [
        "Sirsasana (Headstand)",
        "Sarvangasana (Shoulder Stand)",
        "Adho Mukha Vrksasana (Handstand)",
        "Viparita Karani (Legs Up the Wall Pose)",
        "Halasana (Plow Pose)"
    ],
    "Restorative & Relaxation Poses": [
        "Savasana (Corpse Pose)",
        "Sukhasana (Easy Pose)",
        "Viparita Karani (Legs-Up-the-Wall Pose)",
        "Makarasana (Crocodile Pose)",
        "Shashankasana (Rabbit Pose)"
    ],
    "Pranayama & Meditation Poses": [
        "Padmasana (Lotus Pose)",
        "Vajrasana (Thunderbolt Pose)",
        "Anulom Vilom (Alternate Nostril Breathing)",
        "Kapalabhati (Cleansing Breath)",
        "Bhastrika (Bellows Breath)"
    ]
}

# Streamlit Application
st.sidebar.header("Yoga Poses")
category = st.sidebar.selectbox("Select a Category", options=list(yoga_poses.keys()))
pose_name = st.sidebar.selectbox("Select a Pose", options=yoga_poses[category])

st.header("Yoga Poses Menu")
st.subheader(category)
st.markdown(f"{pose_name}")
st.write("----")

import streamlit as st

# Karate Techniques Dataset with Explanations
karate_techniques = {
    "Karate Stances (Tachikata) - Foundation & Balance": {
        "Heiko Dachi": "Natural stance, feet shoulder-width apart.",
        "Musubi Dachi": "Heels together, toes pointed outward (formal stance).",
        "Zenkutsu Dachi": "Front stance, strong forward lean for strikes.",
        "Kiba Dachi": "Horse stance, strengthens legs and stability.",
        "Kokutsu Dachi": "Back stance, focuses on defense and counter-attacks.",
        "Sanchin Dachi": "Hourglass stance, builds inner strength.",
        "Shiko Dachi": "Wide stance, used in powerful movements.",
        "Neko Ashi Dachi": "Cat stance, keeps weight on the back leg.",
        "Fudo Dachi": "Rooted stance, used in advanced fighting styles.",
        "Tsuru Ashi Dachi": "Crane stance, balances on one leg."
    },
    "Karate Strikes (Uchi & Tsuki) - Offensive Power": {
        "Oi-Zuki": "Lunge punch, generates speed and force.",
        "Gyaku-Zuki": "Reverse punch, powerful and precise.",
        "Kizami-Zuki": "Jab punch, used for speed and setup.",
        "Age-Zuki": "Rising punch, attacks the chin or face.",
        "Ura-Zuki": "Uppercut, powerful short-range strike.",
        "Tate-Zuki": "Vertical fist punch, targets the stomach.",
        "Mawashi-Zuki": "Hook punch, aims at the ribs or head.",
        "Shuto-Uchi": "Knife-hand strike, used for precision.",
        "Tetsui-Uchi": "Hammer fist strike, used for breaking.",
        "Haito-Uchi": "Ridge hand strike, targets the side of the head."
    },
    "Karate Kicks (Geri) - Speed & Agility": {
        "Mae Geri": "Front kick, a basic and effective attack.",
        "Yoko Geri Kekomi": "Side thrust kick, strong and direct.",
        "Yoko Geri Keage": "Side snap kick, fast and surprising.",
        "Mawashi Geri": "Roundhouse kick, commonly used in sparring.",
        "Ushiro Geri": "Back kick, powerful against rear attacks.",
        "Fumikomi Geri": "Stamping kick, used to damage an opponent’s leg.",
        "Hiza Geri": "Knee strike, close-range attack for clinching.",
        "Tobi Geri": "Jump kick, for advanced mobility.",
        "Nidan Geri": "Double kick in mid-air, advanced technique.",
        "Ura Mawashi Geri": "Spinning hook kick, deceptive and powerful."
    },
    "Karate Blocks (Uke) - Defense & Counterattacks": {
        "Jodan Uke": "High block, protects against overhead strikes.",
        "Gedan Barai": "Downward block, deflects low attacks.",
        "Chudan Uke": "Middle block, used against body strikes.",
        "Shuto Uke": "Knife-hand block, precise and sharp.",
        "Haito Uke": "Ridge-hand block, versatile for redirection.",
        "Soto Uke": "Outer forearm block, effective for stopping punches.",
        "Uchi Uke": "Inner forearm block, strong against straight punches.",
        "Morote Uke": "Double-arm block, used for powerful defense.",
        "Kakiwake Uke": "Wedge block, deflects two attacks at once.",
        "Nagashi Uke": "Sweeping block, redirects attacks fluidly."
    },
    "Karate Kata & Sparring (Forms & Combat Drills)": {
        "Heian Shodan": "First beginner Kata, teaches basic stances and strikes.",
        "Heian Nidan": "Second Kata, introduces new blocks and kicks.",
        "Heian Sandan": "Third Kata, focuses on fluidity and transitions.",
        "Bassai Dai": "Advanced Kata, demonstrates powerful movements.",
        "Tekki Shodan": "Teaches strong horse stance and defensive techniques.",
        "Kumite (Sparring)": "Practice fights to refine techniques.",
        "Ippon Kumite": "One-step sparring, training for real fights.",
        "Sanbon Kumite": "Three-step sparring, improves reaction speed.",
        "Jiyu Kumite": "Free sparring, applies full Karate techniques.",
        "Bunkai (Application Practice)": "Interpreting Kata moves for real combat."
    }
}

# Streamlit Application
st.sidebar.header("Karate Techniques")
category = st.sidebar.selectbox("Select a Category", options=list(karate_techniques.keys()))
technique_name = st.sidebar.selectbox("Select a Technique", options=list(karate_techniques[category].keys()))

st.header("Karate Techniques Menu")
st.subheader(category)
st.markdown(f"{technique_name}: {karate_techniques[category][technique_name]}")
st.write("----")

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# ---------------- USER INPUT ----------------
st.sidebar.header("User Input Parameters")
def user_input_features():
    age = st.sidebar.slider("Age", 10, 100, 30)
    bmi = st.sidebar.slider("BMI", 15, 40, 20)
    duration = st.sidebar.slider("Duration (min)", 0, 35, 15)
    heart_rate = st.sidebar.slider("Heart Rate", 60, 130, 80)
    body_temp = st.sidebar.slider("Body Temperature (°C)", 36, 42, 38)
    stress_level = st.sidebar.slider("Stress Level (1-10)", 1, 10, 5)
    gender = st.sidebar.radio("Gender", ("Male", "Female"))
    workout_type = st.sidebar.selectbox("Workout Type", ["Cardio", "Strength Training", "Yoga", "HIIT", "Cycling", "Running"])
    intensity = st.sidebar.selectbox("Intensity Level", ["Low", "Medium", "High"])
    
    gender_val = 1 if gender == "Male" else 0
    return pd.DataFrame({"Age": [age], "BMI": [bmi], "Duration": [duration], "Heart_Rate": [heart_rate], "Body_Temp": [body_temp], "Stress_Level": [stress_level], "Gender_male": [gender_val]}), workout_type, intensity

# Get user inputs first
user_data, workout_type, intensity = user_input_features()


# ---------------- PROGRESS BAR ----------------
st.write("### Your Parameters")
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)
st.dataframe(user_data)

# ---------------- STRESS LEVEL MONITORING ----------------
st.write("### 🧘 Stress Level Monitoring")
if user_data["Stress_Level"].values[0] > 6:
    st.warning("Your stress level is high. Consider relaxation techniques like meditation or deep breathing.")
elif user_data["Stress_Level"].values[0] < 4:
    st.success("Your stress level is low. Keep up the healthy lifestyle!")
else:
    st.info("Your stress level is moderate. Maintaining a balance is key!")

# ---------------- DATA LOADING ----------------
calories = pd.read_csv("calories.csv")
exercise = pd.read_csv("exercise.csv")

data = exercise.merge(calories, on="User_ID")
data.drop(columns=["User_ID"], inplace=True)
data["BMI"] = round(data["Weight"] / ((data["Height"] / 100) ** 2), 2)
data = data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
data = pd.get_dummies(data, drop_first=True)

# Train-test split
X = data.drop("Calories", axis=1)
y = data["Calories"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Model training
model = RandomForestRegressor(n_estimators=1000, max_depth=6, max_features=3, random_state=1)
model.fit(X_train, y_train)

# Align input features with model
user_data = user_data.reindex(columns=X_train.columns, fill_value=0)
calorie_prediction = model.predict(user_data)[0]

# ---------------- OUTPUT DISPLAY ----------------
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🔥 Predicted Calories Burned", value=f"{round(calorie_prediction, 2)} kcal")
with col2:
    st.metric(label="💪 Duration", value=f"{user_data['Duration'].values[0]} min")
with col3:
    st.metric(label="❤ Heart Rate", value=f"{user_data['Heart_Rate'].values[0]} bpm")

# ---------------- WORKOUT DETAILS ----------------
st.write("### 🏋 Workout Details")
st.write(f"Workout Type: {workout_type}")
st.write(f"Intensity Level: {intensity}")

# ---------------- SIMILAR RESULTS ----------------
st.write("### 🔍 Similar Results")
calorie_range = [calorie_prediction - 10, calorie_prediction + 10]
similar_results = data[(data["Calories"] >= calorie_range[0]) & (data["Calories"] <= calorie_range[1])]
# ---------------- SAVE SIMILAR RESULTS TO EXCEL ----------------
def save_similar_results(data):
    file_name = "similar_results.xlsx"
    
    try:
        existing = pd.read_excel(file_name)
        data = pd.concat([existing, data], ignore_index=True)
    except:
        pass  # file not exist first time

    data.to_excel(file_name, index=False)

# Save top 5 similar results
save_similar_results(similar_results.head(5))
st.dataframe(similar_results.sample(5))

# ---------------- GENERAL COMPARISONS ----------------
st.write("---")
st.write("### 📊 General Comparisons")
st.write(f"✔ You are older than {round((data['Age'] < user_data['Age'].values[0]).mean() * 100, 2)}% of users.")
st.write(f"✔ Your exercise duration is longer than {round((data['Duration'] < user_data['Duration'].values[0]).mean() * 100, 2)}% of users.")
st.write(f"✔ Your heart rate is higher than {round((data['Heart_Rate'] < user_data['Heart_Rate'].values[0]).mean() * 100, 2)}% of users.")
st.write(f"✔ Your body temperature is higher than {round((data['Body_Temp'] < user_data['Body_Temp'].values[0]).mean() * 100, 2)}% of users.")
st.write("---")

# ---------------- DAILY WORKOUT GOAL ----------------
st.write("### 🎯 Set Your Daily Workout Goal")
daily_goal = st.number_input("Target Calories to Burn (kcal)", min_value=50, max_value=2000, value=500, step=50)
st.write(f"🏆 Your daily target is {daily_goal} kcal")

# ---------------- WORKOUT HISTORY ----------------
st.write("### 📅 Your Workout History")
if 'workouts' not in st.session_state:
    st.session_state.workouts = []

st.session_state.workouts.append({
    'Date': pd.to_datetime('today').strftime('%Y-%m-%d'),
    'Workout Type': workout_type,
    'Calories Burned': round(calorie_prediction, 2),
    'Duration (min)': user_data['Duration'].values[0]
})
st.dataframe(pd.DataFrame(st.session_state.workouts))

# ---------------- FITNESS RELATED QUESTIONS ----------------
st.write("---")
st.header("Fitness Related Questions")

# Dropdown menu for gym-related topics
topics = [
    "Diet Tips",
    "Exercise Advice",
    "Stress Management",
    "Muscle Gain Tips",
    "Fat Loss Strategies",
    "Workout Recovery",
    "Gym Etiquette",
    "Beginner Tips"
]
selected_topic = st.selectbox("Choose a topic to get advice:", topics)

# Display information based on the selected topic
if st.button("Get Advice"):
    if selected_topic == "Diet Tips":
        st.write("A healthy diet should include a balance of protein, carbohydrates, and fats. Ensure you're drinking enough water and eating plenty of fruits and vegetables.")
    elif selected_topic == "Exercise Advice":
        st.write("Focus on maintaining proper form during exercises. Start light, build consistency, and gradually increase intensity.")
    elif selected_topic == "Stress Management":
        st.write("Incorporate breathing exercises, meditation, or yoga into your routine to manage stress effectively.")
    elif selected_topic == "Muscle Gain Tips":
        st.write("Consume a high-protein diet and ensure a calorie surplus. Train with heavy weights and focus on compound exercises like squats and deadlifts.")
    elif selected_topic == "Fat Loss Strategies":
        st.write("Aim for a calorie deficit by combining regular exercise with mindful eating. Include more cardio and strength training in your workouts.")
    elif selected_topic == "Workout Recovery":
        st.write("Get 7-9 hours of sleep, stay hydrated, and include stretches or foam rolling sessions in your routine to aid recovery.")
    elif selected_topic == "Gym Etiquette":
        st.write("Wipe down equipment after use, re-rack weights, and respect other gym-goers' space and time. Sharing is caring!")
    elif selected_topic == "Beginner Tips":
        st.write("Start slow, focus on learning proper technique, and avoid overtraining. Consistency is key—results take time!")

st.success("🎯 Stay fit and track your progress!")

# ---------------- PERSONALIZED WORKOUT PLAYLIST ----------------
st.write("---")
st.write("### 🎵 Personalized Workout Playlist Generator")

# Predefined workout playlists
playlists = {
    "Cardio": {
        "Low": ["Shape of You - Ed Sheeran", "Counting Stars - OneRepublic", "Get Lucky - Daft Punk"],
        "Medium": ["Can't Stop the Feeling! - Justin Timberlake", "Wake Me Up - Avicii", "Uptown Funk - Bruno Mars"],
        "High": ["Eye of the Tiger - Survivor", "Stronger - Kanye West", "Lose Yourself - Eminem"]
    },
    "Strength Training": {
        "Low": ["Stressed Out - Twenty One Pilots", "Take Me to Church - Hozier", "Photograph - Ed Sheeran"],
        "Medium": ["Believer - Imagine Dragons", "Radioactive - Imagine Dragons", "Thunderstruck - AC/DC"],
        "High": ["Till I Collapse - Eminem", "Power - Kanye West", "Remember the Name - Fort Minor"]
    },
    "Yoga": {
        "Low": ["Weightless - Marconi Union", "A Thousand Years - Christina Perri", "Hallelujah - Jeff Buckley"],
        "Medium": ["Sunset Lover - Petit Biscuit", "Let Her Go - Passenger", "The Scientist - Coldplay"],
        "High": ["Fix You - Coldplay", "River Flows in You - Yiruma", "Comptine d'un autre été - Yann Tiersen"]
    },
    "HIIT": {
        "Low": ["Counting Stars - OneRepublic", "Love Me Like You Do - Ellie Goulding", "Titanium - David Guetta"],
        "Medium": ["Stronger - Kanye West", "Can't Hold Us - Macklemore", "Uptown Funk - Bruno Mars"],
        "High": ["Till I Collapse - Eminem", "Eye of the Tiger - Survivor", "Remember the Name - Fort Minor"]
    },
    "Cycling": {
        "Low": ["Take Me to Church - Hozier", "Castle on the Hill - Ed Sheeran", "Let Her Go - Passenger"],
        "Medium": ["Uptown Funk - Bruno Mars", "Believer - Imagine Dragons", "Radioactive - Imagine Dragons"],
        "High": ["Lose Yourself - Eminem", "Stronger - Kanye West", "Can't Stop - Red Hot Chili Peppers"]
    },
    "Running": {
        "Low": ["See You Again - Wiz Khalifa", "Chasing Cars - Snow Patrol", "Thinking Out Loud - Ed Sheeran"],
        "Medium": ["Feel It Still - Portugal. The Man", "Wake Me Up - Avicii", "Don't Stop Believin' - Journey"],
        "High": ["Eye of the Tiger - Survivor", "Till I Collapse - Eminem", "Born to Run - Bruce Springsteen"]
    }
}

# Display playlist based on selection
if workout_type in playlists and intensity in playlists[workout_type]:
    playlist = playlists[workout_type][intensity]
    st.write(f"🎧 Your Workout Playlist for *{workout_type} ({intensity})* Intensity:")
    for song in playlist:
        search_url = f"https://www.youtube.com/results?search_query={'+'.join(song.split())}"
        st.markdown(f"- [{song}]({search_url}) 🎶")