import tkinter as tk
from playsound import playsound  # Install with: pip install playsound
import random

# Theme colors (blue themed kita)
THEME_BG = "#032d4d"  # background
THEME_FG = "white"  # text
BUTTON_BG = "#508ABA"  # kat kulay it button mismo atecco
BUTTON_FG = "white"  # kat letters sa sueod it buttons
ENTRY_BG = "#021024"  # kat ginatypan raya
ENTRY_HIGHLIGHT = "#00F0FF"  # border for entry
FONT = ("Consolas", 12)  # mas nami kuno ro consolas for games


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
        self.root.title("Spelling Game")
        self.root.geometry("600x400")
        self.root.configure(bg=THEME_BG)

        # Initialize data structures
        self.word_queue = Queue()  # Queue for words
        self.attempt_stack = Stack()  # Stack for user attempts (e.g., (word, is_correct))

        # Words to be spelled with definitions and audio files
        # dictionary
        self.words = [
            {'word': 'cell','definition': 'The basic unit of life in all living organisms.','audio': 'musics1.mp3'},
            {'word': 'nucleus','definition': 'The control center of a cell that contains DNA.','audio': 'musics2.mp3'},
            {'word': 'osmosis', 'definition': 'The movement of water across a membrane from high to low concentration.','audio': 'musics3.mp3'},
            {'word': 'mitochondria','definition': 'Organelles that produce energy for the cell; known as the "powerhouse."','audio': 'musics4.mp3'},
            {'word': 'photosynthesis','definition': 'The process by which plants make food using sunlight, water, and carbon dioxide.','audio': 'musics5.mp3'},
            {'word': 'chlorophyll','definition': 'The green pigment in plants that captures sunlight for photosynthesis.','audio': 'musics6.mp3'},
            {'word': 'enzyme', 'definition': 'A protein that speeds up chemical reactions in the body.','audio': 'musics7.mp3'},
            {'word': 'genetics','definition': 'The study of heredity and how traits are passed from parents to offspring','audio': 'musics8.mp3'},
            {'word': 'mutation', 'definition': 'A change in the DNA sequence that can affect traits.','audio': 'musics9.mp3'},
            {'word': 'ecology','definition': 'The study of how organisms interact with each other and their environment.','audio': 'musics10.mp3'},
            {'word': 'habitat', 'definition': 'The natural home or environment of an organism.', 'audio': 'musics11.mp3'},
            {'word': 'adaptation', 'definition': 'A trait helps an organism survive in its environment.','audio': 'musics12.mp3'},
            {'word': 'species', 'definition': 'A group of organisms survive in its environment.','audio': 'musics13.mp3'},
            {'word': 'vertebrate', 'definition': 'An animal with backbone.', 'audio': 'musics14.mp3'},
            {'word': 'pneumonoultramicroscopicsilicovolcanoconiosis','definition': 'A lung disease caused by inhaling extremely fine silicate or quartz dust, often found near volcanoes or in mining environments.','audio': 'musics15.mp3'},
        ]

        self.current_word = None  # Current word being played
        self.attempts_left = 1  # Attempts for each word
        self.score = 0  # Overall score
        self.correct_words = []  # List to track correct words with definitions
        self.all_inputs = []  # List to track all user inputs

        # UI Elements

        self.definition_label = tk.Label(root, text="Definition will appear here.", wraplength=300, bg=THEME_BG,fg=THEME_FG, font=FONT)
        self.definition_label.pack(pady=10)

        self.attempts_label = tk.Label(root, text=f"Attempts left: {self.attempts_left}", bg=THEME_BG, fg=THEME_FG,font=FONT)
        self.attempts_label.pack()

        self.play_sound_button = tk.Button(root, text="Play Sound", command=self.play_sound, bg=BUTTON_BG, fg=BUTTON_FG,font=FONT)  # forda sound button
        self.play_sound_button.pack(pady=5)

        self.entry = tk.Entry(root, width=30, bg=ENTRY_BG, fg=BUTTON_FG, font=FONT, highlightbackground=ENTRY_HIGHLIGHT,highlightthickness=2)  # Textbox for user input
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="Enter", command=self.check_answer, bg=BUTTON_BG, fg=BUTTON_FG,font=FONT)
        self.submit_button.pack(pady=5)

        self.score_label = tk.Label(root, text=f"Score: {self.score}", bg=THEME_BG, fg=THEME_FG, font=FONT)
        self.score_label.pack(pady=10)

        # Single skip button
        self.skip_button = tk.Button(root, text="Skip", command=self.skip_word, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)
        self.skip_button.pack(pady=10)

        # Start the game with the first word
        self.start_game()

    def start_game(self):
        # Shuffle the words using random
        random.shuffle(self.words)

        # Enqueue the shuffled words into the queue
        for word in self.words:
            self.word_queue.enqueue(word)

        # # Select 10 random words from the 15
        # selected_words = random.sample(self.words, 10)
        # # Enqueue the selected words into the queue
        # for word in selected_words:
        #     self.word_queue.enqueue(word)


        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.correct_words = []  # Reset correct words list
        self.all_inputs = []  # Reset all inputs list
        self.attempt_stack = Stack()  # Reset stack
        self.getnext_Word()

    def getnext_Word(self):
        if not self.word_queue.is_empty():
            self.current_word = self.word_queue.dequeue()
            self.attempts_left = 1  # Reset attempts for new word
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

            self.all_inputs.append(user_input)  # Track all user inputs

            is_correct = user_input == correct_word  # Check if correct

            # Push the attempt to the stack  (word, is_correct)
            self.attempt_stack.push((self.current_word['word'], is_correct))

            if is_correct:
                self.correct_words.append({'word': self.current_word['word'],
                                           'definition': self.current_word['definition']})  # Track correct words
                self.score += 1  # Increment score for correct answer
                self.score_label.config(text=f"Score: {self.score}")  # Update score label
                self.definition_label.config(text=f"Correct! Definition: {self.current_word['definition']}")
                self.getnext_Word()  # Automatically proceed to next word
            else:
                self.attempts_left -= 1  # if mali minus 1 do attempts
                if self.attempts_left >=0:
                    self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
                    self.definition_label.config(
                        text=f"\nIncorrect. Try again! \nAttempts left: {self.attempts_left}. \nDefinition: {self.current_word['definition']}")
                else:
                    self.definition_label.config(
                        text=f"Out of attempts. The correct word is: {self.current_word['word']}. Definition: {self.current_word['definition']}")
                    self.getnext_Word()  # Proceed to next word after showing correct pag naubos ing free trial ganern

    def skip_word(self):
        if self.current_word:
            # Skip the current word and move to the next
            self.getnext_Word()

    def end_game(self):
        # Build summary text
        summary = f"Game Over! Overall Score: {self.score}\n\nCorrect Words:\n"
        for item in self.correct_words:
            summary += f"{item['word']}: {item['definition']}\n"
        summary += "\nAll User Inputs:\n" + "\n".join(self.all_inputs)

        self.definition_label.config(text=summary)
        self.play_sound_button.destroy()  # Remove playsound button
        self.entry.destroy()  # Remove textbox
        self.submit_button.destroy()  # Remove enter button
        self.attempts_label.config(text="")
        self.skip_button.config(text="Restart", command=self.replay_game)  # Replace with restart button

        # Optionally, review the stack (e.g., print the last attempt)
        if not self.attempt_stack.is_empty():
            last_attempt = self.attempt_stack.peek()  # Peek at the top of the stack
            print(f"Last attempt: Word '{last_attempt[0]}' was {'correct' if last_attempt[1] else 'incorrect'}")

        print(f"Final Score: {self.score} ")  # Console output for debugging

    def replay_game(self):  # para mag uman
        # Recreate removed UI elements
        self.play_sound_button = tk.Button(self.root, text="Play Sound", command=self.play_sound, bg=BUTTON_BG,                                   fg=BUTTON_FG, font=FONT)
        self.play_sound_button.pack(pady=5)
        self.entry = tk.Entry(self.root, width=30, bg=ENTRY_BG, fg=BUTTON_FG, font=FONT,highlightbackground=ENTRY_HIGHLIGHT, highlightthickness=2)
        self.entry.pack(pady=5)
        self.submit_button = tk.Button(self.root, text="Enter", command=self.check_answer, bg=BUTTON_BG, fg=BUTTON_FG,                     font=FONT)
        self.submit_button.pack(pady=5)


        # Reset the game
        self.word_queue = Queue()  # Reset queue
        self.attempt_stack = Stack()  # Reset stack
        self.score = 0  # ibalik sa zero do score
        self.correct_words = []  # Reset correct words list
        self.all_inputs = []  # Reset all inputs list
        self.score_label.config(text=f"Score: {self.score}")
        self.definition_label.config(text="Definition will appear here.")
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.skip_button.config(text="Skip", command=self.skip_word)  # Reset skip button
        self.start_game()  # kara euman nag uman it hampang


if __name__ == "__main__":
    root = tk.Tk()  # main window para kay tkinter
    game = SpellingGame(root)  # instantiate kuno
    root.mainloop()  # starts the Tkinter event loop
