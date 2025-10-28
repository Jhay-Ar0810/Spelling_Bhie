import tkinter as tk
from playsound import playsound  # Install with: pip install playsound
import random


# Theme colors
THEME_BG = "#FFC0CB"  # pink background
THEME_FG = "#00FF00"  # green text
BUTTON_BG = "white"
BUTTON_FG = "black"
ENTRY_BG = "white"
ENTRY_HIGHLIGHT = "#FFD700"  # Gold border for entry
FONT = ("Bookman Old Style", 12)
# Abstract Data Structure 1: Queue (for managing words to be spelled)
class Queue:
    def __init__(self):
        self.items = []  # Internal list to store items

    def enqueue(self, item):
        self.items.append(item)  # Add item to the end

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # Remove and return from the front

    def is_empty(self):
        return len(self.items) == 0  # Check if empty


# Abstract Data Structure 2: Stack (for tracking user attempts)
class Stack:
    def __init__(self):
        self.items = []  # Internal list to store items

    def push(self, item):
        self.items.append(item)  # Add item to the top

    def pop(self):
        if not self.is_empty():
            return self.items.pop()  # Remove and return from the top

    def is_empty(self):
        return len(self.items) == 0  # Check if empty

    def peek(self):
        if not self.is_empty():
            return self.items[-1]  # View the top item without removing


class SpellingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Spelling Game")
        self.root.geometry("600x400")
        self.root.configure(bg=THEME_BG)

        # Initialize data structures
        self.word_queue = Queue()  # Queue for words
        self.attempt_stack = Stack()  # Stack for user attempts (e.g., (word, is_correct))

        # Sample words with definitions and audio files
        self.words = [
            {'word': 'apple', 'definition': 'A fruit that is typically red or green.', 'audio': 'music1.mp3'},
            {'word': 'banana', 'definition': 'A long curved fruit with a yellow skin.', 'audio': 'banana.mp3'},
            {'word': 'cherry', 'definition': 'A small, round stone fruit that is usually red.', 'audio': 'cherry.mp3'}
            # Add more words as needed. Ensure audio files exist in the same directory.
        ]

        self.current_word = None  # Current word being played
        self.attempts_left = 3  # Attempts for each word
        self.score = 0  # Overall score

        # UI Elements

        self.definition_label = tk.Label(root, text="Definition will appear here.", wraplength=300, bg=THEME_BG, fg=THEME_FG, font=FONT)
        self.definition_label.pack(pady=10)

        self.attempts_label = tk.Label(root, text=f"Attempts left: {self.attempts_left}", bg=THEME_BG, fg=THEME_FG, font=FONT)
        self.attempts_label.pack()

        self.play_sound_button = tk.Button(root, text="Play Sound", command=self.play_sound, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT) #forda sound button
        self.play_sound_button.pack(pady=5)

        self.entry = tk.Entry(root, width=30, bg=ENTRY_BG, fg=BUTTON_FG, font=FONT, highlightbackground=ENTRY_HIGHLIGHT, highlightthickness=2)  # Textbox for user input
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit Answer", command=self.check_answer, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)
        self.submit_button.pack(pady=5)

        self.score_label = tk.Label(root, text=f"Score: {self.score}", bg=THEME_BG, fg=THEME_FG, font=FONT)
        self.score_label.pack(pady=10)

        # Buttons for end game
        self.exit_button = tk.Button(root, text="Exit", command=self.root.quit, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT, state='disabled')
        self.exit_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.replay_button = tk.Button(root, text="Replay", command=self.replay_game, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT, state='disabled')
        self.replay_button.pack(side=tk.RIGHT, padx=20, pady=10)

        # Start the game with the first word
        self.start_game()

    def start_game(self):
        # Shuffle the words using random
        random.shuffle(self.words)

        # Enqueue the shuffled words into the queue
        for word in self.words:
            self.word_queue.enqueue(word)

        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.attempt_stack = Stack()  # Reset stack
        self.get_next_word()

    def get_next_word(self):
        if not self.word_queue.is_empty():
            self.current_word = self.word_queue.dequeue()
            self.attempts_left = 3  # Reset attempts for new word
            self.definition_label.config(text=f"Definition: {self.current_word['definition']}")
            self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
            self.entry.delete(0, tk.END)  # Clear the textbox
        else:
            self.end_game()

    def play_sound(self):
        if self.current_word:
            try:
                playsound(self.current_word['audio'])  # Play the audio file
            except Exception as e:
                self.definition_label.config(text=f"Error playing sound: {e}")

    def check_answer(self):
        if self.current_word:
            user_input = self.entry.get().strip().lower()  # Get user input and convert to lowercase
            correct_word = self.current_word['word'].lower()  # Convert correct word to lowercase for comparison

            is_correct = user_input == correct_word  # Check if correct

            # Push the attempt to the stack (e.g., (word, is_correct))
            self.attempt_stack.push((self.current_word['word'], is_correct))

            if is_correct:
                self.score += 1  # Increment score for correct answer
                self.score_label.config(text=f"Score: {self.score}")  # Update score label
                self.definition_label.config(text=f"Correct! Definition: {self.current_word['definition']}")
                self.get_next_word()  # Automatically proceed to next word
            else:
                self.attempts_left -= 1 #if mali minus 1 do attempts
                if self.attempts_left > 0:
                    self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
                    self.definition_label.config(text=f"Incorrect. Try again! Attempts left: {self.attempts_left}. Definition: {self.current_word['definition']}")
                else:
                    self.definition_label.config(text=f"Out of attempts. The correct word is: {self.current_word['word']}. Definition: {self.current_word['definition']}")
                    self.get_next_word()  # Proceed to next word after showing correct pag naubos ing free trial ganern

    def end_game(self):
        self.definition_label.config(text=f"Game Over! Overall Score: {self.score}")
        self.play_sound_button.config(state='disabled')  # Disable buttons if natapos na ang lahat duea eon guro kara tanan ro buttons
        self.submit_button.config(state='disabled')
        self.entry.config(state='disabled')
        self.attempts_label.config(text="")
        self.exit_button.config(state='normal')
        self.replay_button.config(state='normal')

        # Optionally, review the stack (e.g., print the last attempt)
        if not self.attempt_stack.is_empty():
            last_attempt = self.attempt_stack.peek()  # Peek at the top of the stack
            print(f"Last attempt: Word '{last_attempt[0]}' was {'correct' if last_attempt[1] else 'incorrect'}")

        print(f"Final Score: {self.score}")  # Console output for debugging

    def replay_game(self):   #para mag uman, hindi lang dun basta basta matatapos ang ralo
        # Reset the game
        self.word_queue = Queue()  # Reset queue
        self.attempt_stack = Stack()  # Reset stack
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.definition_label.config(text="Definition will appear here.")
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.play_sound_button.config(state='normal')
        self.submit_button.config(state='normal')
        self.entry.config(state='normal')
        self.exit_button.config(state='disabled')
        self.replay_button.config(state='disabled')
        self.start_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = SpellingGame(root)
    root.mainloop()
