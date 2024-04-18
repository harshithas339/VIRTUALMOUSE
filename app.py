from flask import Flask, render_template, jsonify
import psutil
import subprocess
import os

app = Flask(__name__)

# Variable to store the subprocess object
gesture_controller_process = None

# Route for rendering the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route for rendering the rules.html page
@app.route('/rules.html')
def rules():
    return render_template('rules.html')

# Function to start the Gesture Controller
def start_gesture_controller():
    global gesture_controller_process
    # Check if the gesture_controller_process is already running
    if gesture_controller_process is None or gesture_controller_process.poll() is not None:
        # Run the Gesture_Controller.py file in a separate process
        gesture_controller_process = subprocess.Popen(['python', 'Gesture_Controller.py'])
        return True
    return False

# Route for starting the Gesture Controller
@app.route('/start', methods=['POST'])
def start():
    success = start_gesture_controller()
    if success:
        return jsonify({'message': 'Gesture Controller started successfully!'}), 200
    else:
        return jsonify({'message': 'Failed to start Gesture Controller!'}), 500

# Function to stop the Gesture Controller
def stop_gesture_controller():
    global gesture_controller_process
    # Check if the gesture_controller_process is running
    if gesture_controller_process is not None and gesture_controller_process.poll() is None:
        # Terminate the process
        gesture_controller_process.terminate()
        gesture_controller_process = None
        return True
    return False

# Route for stopping the Gesture Controller
@app.route('/stop', methods=['POST'])
def stop():
    success = stop_gesture_controller()
    if success:
        return jsonify({'message': 'Gesture Controller stopped successfully!'}), 200
    else:
        return jsonify({'message': 'Failed to stop Gesture Controller!'}), 500

if __name__ == '__main__':
    app.run(debug=True)
