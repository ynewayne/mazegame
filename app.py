from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/single_player')
def single_player():
    # Run the single player mode Python code in a separate window
    # Note: This approach may not work for all Python game codes
    # You may need to adapt the Python code to run in a web environment
    # using libraries like Pygame_sdl2 or Pygame.js
    # For demonstration purposes, let's assume the Python code is run locally
    import subprocess
    subprocess.Popen(['python', 'maze/spmd.py'])

    return 'Single Player Mode launched'

@app.route('/multiplayer')
def multiplayer():
    # Similar to the single player route, launch the multiplayer mode Python code
    return 'Multiplayer Mode launched'

if __name__ == '__main__':
    app.run(debug=True)
