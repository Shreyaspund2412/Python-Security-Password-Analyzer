🔒 Advanced Password Strength Analyzer (Python / Tkinter)
A comprehensive cybersecurity tool designed to assess password strength using multi-layered, mathematically rigorous metrics.

✨ Key Features & Cybersecurity Achievements
Multi-layered Security Check: Developed a system that combines a basic complexity score (0-6) with a scientific Shannon Entropy calculation for robust analysis.

Dictionary Attack Prevention: Implemented a critical pre-check against a list of known compromised passwords (common_passwords.txt), instantly triggering a "CRITICAL FAIL" if the input is found.

Shannon Entropy Calculation: Mathematically quantifies the password's randomness (H=L×log 
2
​
 (R)), providing a precise estimate of the time required for a brute-force attack (e.g., "Centuries").

Real-Time Tkinter GUI: Engineered a user-friendly desktop application featuring a color-coded progress bar and dynamic labels that update instantly as the user types.

💡 Technical Deep Dive (The "How")
The application is built in Python, leveraging powerful standard libraries:

Python (Core Logic): Handles all security checks, scoring, and file operations.

Tkinter/ttk (GUI): Provides the user interface, including the password entry box and the color-changing strength meter.

re (Regular Expressions): Used extensively to check for character diversity (uppercase, numbers, special characters).

math (Logarithm): Essential for calculating the Shannon Entropy value.

Core Logic: All analysis is tied to the <KeyRelease> event on the input box for instantaneous results.

🚀 How to Run the Application
This application runs locally and requires a standard Python 3 installation.

Download Files: Clone this repository or ensure you have the following two files in the same folder: gui_checker.py and common_passwords.txt.

Execute: Open your terminal in the project directory and run the main file:

python gui_checker.py

Test Scenarios: Try typing a complex password (e.g., MyL0ngP@ssphrase) vs. a common password (e.g., password) to see the difference between the VERY STRONG and CRITICAL FAIL states.

👨‍💻 Project Structure
The project is structured for clean separation of concerns:

gui_checker.py: Contains all the application logic, the PasswordApp class, and the Tkinter setup.

common_passwords.txt: The external file used by the dictionary attack simulation function.