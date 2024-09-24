from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'hangman_secret_key'

# List of words to choose from
WORDS = ['python', 'flask', 'javascript', 'developer',
         'hangman', 'programming', 'machinelearning',
         'kigali', 'Rwanda', 'love', 'skip', 'computer',
         'bread', 'spoon', 'car', 'bike', 'country', 'june',
         'bottle', 'phone', 'laptop', 'coffee', 'school',
         'keyboard', 'music', 'pencil', 'notebook', 'camera',
         'city', 'holiday', 'internet', 'elephant', 'tree']



# Initialize game state
def initialize_game():
    word = random.choice(WORDS)
    session['word'] = word
    session['guessed'] = ['_'] * len(word)
    session['guessed'][0] = word[0]   # Reveal the first letter
    session['guessed'][-1] = word[-1] # Reveal the last letter
    session['first_letter'] = word[0] # Store first letter in session
    session['last_letter'] = word[-1] # Store last letter in session
    session['attempts'] = 6
    session['incorrect_guesses'] = []


# Route for home page to start/restart the game
@app.route('/')
def index():
    if 'word' not in session:
        initialize_game()
    return render_template('index.html', word=session['guessed'], attempts=session['attempts'],
                           incorrect=session['incorrect_guesses'])


# Handle guess input and game logic
@app.route('/guess', methods=['POST'])
def guess():
    if 'word' not in session:
        return redirect(url_for('index'))

    letter = request.form['letter'].lower()
    word = session['word']
    guessed = session['guessed']
    incorrect_guesses = session['incorrect_guesses']

    # Check if the letter is in the word
    if letter in word:
        # Update the guessed list for every occurrence of the letter
        for i, char in enumerate(word):
            if char == letter:
                guessed[i] = letter
    else:
        # Handle incorrect guess
        if letter not in incorrect_guesses:
            incorrect_guesses.append(letter)
            session['attempts'] -= 1

    # Check if the game is won or lost
    if session['attempts'] <= 0:
        return redirect(url_for('lost'))
    elif '_' not in guessed:
        return redirect(url_for('won'))

    session['guessed'] = guessed
    session['incorrect_guesses'] = incorrect_guesses
    return redirect(url_for('index'))


# Win route
@app.route('/won')
def won():
    return render_template('won.html', word=session['word'])


# Lose route
@app.route('/lost')
def lost():
    return render_template('lost.html', word=session['word'])


# Reset game route
@app.route('/reset')
def reset():
    initialize_game()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
