import speech_recognition as sr
import time
import threading

# Function to calculate WPM and words
def calculate_wpm(text, duration_seconds):
    words = len(text.split())
    minutes = duration_seconds / 60
    wpm = words / minutes if minutes > 0 else 0
    return round(wpm, 2), words

# Function to give feedback on speaking speed
def give_feedback(wpm):
    if wpm < 110:
        return "🐢 You're speaking a bit slow."
    elif 110 <= wpm <= 160:
        return "✅ You're speaking at a good pace!"
    else:
        return "🚀 You're speaking quite fast!"

# Function to get recording time input from the user
def get_recording_time():
    while True:
        try:
            time_input = int(input("⏱️ Enter how many seconds you want to record (10 to 60): "))
            if 10 <= time_input <= 60:
                return time_input
            else:
                print("⚠️ Please enter a number between 10 and 60.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")

# Function to show countdown timer
def countdown_timer(duration_seconds):
    for remaining_time in range(duration_seconds, 0, -1):
        print(f"\r⏳ Time left: {remaining_time} seconds", end="")
        time.sleep(1)
    print("\n🎤 Time's up!")

# Main function
def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Adjust the sensitivity of the microphone for better accuracy
    print("🎤 Please wait. Calibrating microphone...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("🔧 Microphone calibrated.")

    # Get the recording time from the user
    record_time = get_recording_time()
    print(f"🔴 Start speaking. I’ll listen for {record_time} seconds...")

    # Start the countdown timer in a separate thread
    timer_thread = threading.Thread(target=countdown_timer, args=(record_time,))
    timer_thread.start()

    # Timeout set for the recognizer, adjust based on needs
    with mic as source:
        try:
            start_time = time.time()
            audio = recognizer.listen(source, timeout=record_time, phrase_time_limit=record_time)
            end_time = time.time()
        except sr.WaitTimeoutError:
            print("❌ Timeout reached without speech detected.")
            return

    # Wait for the timer thread to finish
    timer_thread.join()

    duration = end_time - start_time

    try:
        print("📝 Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        wpm, word_count = calculate_wpm(text, duration)

        print("\n--- 📊 Results ---")
        print(f"🗣️ You said: \"{text}\"")
        print(f"🔢 Word count: {word_count}")
        print(f"⏱️ Duration: {round(duration, 2)} seconds")
        print(f"📈 WPM (Words per Minute): {wpm}")
        print(f"💬 Feedback: {give_feedback(wpm)}")

    except sr.UnknownValueError:
        print("❌ Could not understand the speech.")
    except sr.RequestError as e:
        print(f"❌ Could not request results from Google Speech Recognition service; {e}")

# Run the program
if __name__ == "__main__":
    main()
