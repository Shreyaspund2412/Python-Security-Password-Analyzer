import re
import math
import tkinter as tk
from tkinter import ttk 
from typing import Tuple, List

# --- Configuration ---
MIN_LENGTH = 8
MAX_SCORE = 6
DICTIONARY_FILE = 'common_passwords.txt'

# --- 1. Dictionary Check Function (For CRITICAL FAIL) ---
def check_common_password(password: str) -> bool:
    """Checks if the password exists in the list of common passwords."""
    try:
        with open(DICTIONARY_FILE, 'r') as f:
            # Use a set for fast lookup
            common_passwords = {line.strip().lower() for line in f}
    except FileNotFoundError:
        # NOTE: We skip printing the warning in the GUI version to keep the console clean.
        # This function returns False, allowing the complexity check to run.
        return False

    # Check against the dictionary in lowercase
    return password.lower() in common_passwords

# --- 2. Shannon Entropy Calculation ---
def calculate_entropy(password: str) -> Tuple[int, str]:
    """Calculates Shannon Entropy (bits) and estimates time to crack."""
    
    pool_size = 0
    if re.search(r'[a-z]', password):
        pool_size += 26
    if re.search(r'[A-Z]', password):
        pool_size += 26
    if re.search(r'[0-9]', password):
        pool_size += 10
    if re.search(r'[^a-zA-Z0-9\s]', password):
        pool_size += 32 
    
    length = len(password)
    
    if pool_size == 0 or length == 0:
        return 0, "N/A"

    # Calculate Entropy (H = L * log2(R))
    entropy_bits = length * math.log2(pool_size)
    
    # Estimate Time to Crack (Simplified)
    crack_time = ""
    if entropy_bits < 60:
        crack_time = "Milliseconds"
    elif entropy_bits < 75:
        crack_time = "Minutes to Hours"
    elif entropy_bits < 90:
        crack_time = "Days to Weeks"
    elif entropy_bits < 110:
        crack_time = "Years to Decades"
    else:
        crack_time = "Centuries (Highly Secure)"
        
    return round(entropy_bits, 2), crack_time


# --- 3. Main Scoring Function (Complexity Check) ---
def check_password_strength(password: str) -> Tuple[int, List[str]]:
    """Evaluates a password based on complexity rules."""
    score = 0
    feedback = []

    length = len(password)
    if length < MIN_LENGTH:
        feedback.append(f"Password is too short (< {MIN_LENGTH} chars).")
        return 0, feedback 
    
    # Add points for length
    if length >= 14:
        score += 2
    elif length >= MIN_LENGTH:
        score += 1
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Missing Uppercase (A-Z).")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Missing Lowercase (a-z).")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Missing Numbers (0-9).")

    if re.search(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|]', password): 
        score += 2 
    else:
        feedback.append("Missing Special Characters (!@#$).")

    return score, feedback

# --- 4. GUI APPLICATION CLASS ---

class PasswordApp:
    def __init__(self, master):
        self.master = master
        master.title("Security Password Checker v1.2")
        master.geometry("450x300")
        
        # Style setup for colored progress bar
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # Define custom styles for colors
        self.style.map('green.Horizontal.TProgressbar', background=[('active', 'green'), ('!disabled', 'green')])
        self.style.map('blue.Horizontal.TProgressbar', background=[('active', 'blue'), ('!disabled', 'blue')])
        self.style.map('orange.Horizontal.TProgressbar', background=[('active', 'orange'), ('!disabled', 'orange')])
        self.style.map('red.Horizontal.TProgressbar', background=[('active', 'red'), ('!disabled', 'red')])
        
        # --- GUI Elements Layout ---
        
        ttk.Label(master, text="Secure Password Checker", font=('Arial', 16, 'bold')).pack(pady=10)

        ttk.Label(master, text="Enter Password:").pack()
        
        # Password Input (show='*' hides the characters)
        self.password_entry = ttk.Entry(master, show='*', width=40, font=('Arial', 11))
        self.password_entry.pack(pady=5)
        
        # Bind the analysis function to the KeyRelease event for real-time check
        self.password_entry.bind("<KeyRelease>", self.analyze_password)

        # Visual Meter (Progress Bar)
        self.progress_bar = ttk.Progressbar(master, orient='horizontal', length=350, mode='determinate', style='red.Horizontal.TProgressbar')
        self.progress_bar.pack(pady=10)
        self.progress_bar['value'] = 0

        # Feedback Labels
        self.rating_label = ttk.Label(master, text="Rating: Start Typing...", font=('Arial', 12, 'bold'))
        self.rating_label.pack()
        
        self.entropy_label = ttk.Label(master, text="Entropy: N/A | Crack Time: N/A", font=('Arial', 10))
        self.entropy_label.pack(pady=5)
        
        self.suggestion_label = ttk.Label(master, text="", foreground='red', font=('Arial', 9, 'italic'))
        self.suggestion_label.pack(pady=5)
        
        # Ensure the app loop starts
        master.protocol("WM_DELETE_WINDOW", master.destroy)
        master.mainloop()

    # --- Real-Time Analysis Method ---
    def analyze_password(self, event):
        password = self.password_entry.get()

        # Handle empty password case
        if not password:
            self.rating_label.config(text="Rating: Start Typing...", foreground='black')
            self.progress_bar['value'] = 0
            self.entropy_label.config(text="Entropy: N/A | Crack Time: N/A")
            self.suggestion_label.config(text="")
            return

        # 1. CRITICAL DICTIONARY CHECK
        if check_common_password(password):
            self.progress_bar['value'] = 100
            self.progress_bar.config(style="red.Horizontal.TProgressbar")
            self.rating_label.config(text="🔴 CRITICAL FAIL: KNOWN PASSWORD", foreground='red')
            self.entropy_label.config(text="Security: INSTANTLY WEAK")
            self.suggestion_label.config(text="🛑 Change Immediately! Vulnerable to dictionary attack.", foreground='red')
            return

        # 2. COMPLEXITY AND ENTROPY CALCULATION
        final_score, suggestions = check_password_strength(password)
        entropy_bits, crack_estimate = calculate_entropy(password)

        # 3. DETERMINE RATING and COLOR based on complexity score
        if final_score >= 6:
            rating_text = "💪 VERY STRONG"
            bar_color = "green"
            progress_value = 100
        elif final_score >= 4:
            rating_text = "✅ STRONG"
            bar_color = "blue"
            progress_value = 75
        elif final_score >= 2:
            rating_text = "🟠 MEDIUM"
            bar_color = "orange"
            progress_value = 50
        else:
            rating_text = "🔴 WEAK"
            bar_color = "red"
            progress_value = 25
            
        # 4. UPDATE GUI
        
        # Update Progress Bar Color and Value
        self.progress_bar.config(style=f"{bar_color}.Horizontal.TProgressbar")
        self.progress_bar['value'] = progress_value
        
        # Update Labels
        self.rating_label.config(text=f"Rating: {rating_text} ({final_score}/{MAX_SCORE})", foreground=bar_color)
        self.entropy_label.config(text=f"Entropy: {entropy_bits} bits | Est. Crack Time: {crack_estimate}")

        if suggestions and final_score < MAX_SCORE:
            # Display the first suggestion to guide the user
            self.suggestion_label.config(text=f"Hint: {suggestions[0]}", foreground='orange')
        else:
            self.suggestion_label.config(text="🎉 Highly Secure!", foreground='green')


# --- FINAL EXECUTION ---
if __name__ == '__main__':
    root = tk.Tk()
    app = PasswordApp(root)