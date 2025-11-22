import tkinter as tk  # nickname na ro tk
from playsound import playsound  # Install with: pip install playsound o install lat specific version it playsound
import random
import time  # For delaying the intro
import os  # For file operations (high score)
from constants import THEME_FG, BUTTON_BG, BUTTON_FG, ENTRY_BG, ENTRY_HIGHLIGHT, FONT
from dataStructures import Queue, Stack

class SpellingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Spelling Game")
        self.root.geometry("600x400")


        # Load background image
        try:
            self.bg_image = tk.PhotoImage(file='wizardbg.png')
        except:
            self.bg_image = None  # Fallback if image not found

        # Create canvas for background
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        if self.bg_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # High score file
        self.high_score_file = 'high_score.txt'
        self.high_score = self.load_high_score()

        # Initialize data structures
        self.word_queue = Queue()  # Queue for words
        self.attempt_stack = Stack()  # Stack for user attempts ((word, is_correct))

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

        self.current_word = None  # Current word being played, para random do first ano
        self.lives = 3  # Overall lives (replacing attempts)
        self.score = 0  # Overall score
        self.correct_words = []  # List to track correct words with definitions (kept for internal use, but not displayed)
        self.all_inputs = []  # List to track all user inputs (kept for internal use, but not displayed)

        # Intro UI Elements (shown first)
        self.intro_label = tk.Label(self.canvas, text="Welcome to the Spelling Adventure!\n\nEmbark on a journey through the world of biology.\nSpell the words correctly to score points.\nYou have 3 lives (🍃🍃🍃).\nWrong answers or skips will cost a life.\n\nGet ready...", wraplength=500, bg="#C38888", fg=THEME_FG, font=FONT)
        self.canvas.create_window(300, 150, window=self.intro_label)
        self.start_button = tk.Button(self.canvas, text="Start Game", command=self.start_intro, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)
        self.canvas.create_window(300, 250, window=self.start_button)

        # Game UI Elements (hidden initially)
        self.definition_label = tk.Label(self.canvas, text="", wraplength=300, bg="#C38888", fg=THEME_FG, font=FONT)
        self.lives_label = tk.Label(self.canvas, text=f"Lives: {self.get_lives_display()}", bg="#C38888", fg=THEME_FG, font=FONT)
        self.play_sound_button = tk.Button(self.canvas, text="Play Sound", command=self.play_sound, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)
        self.entry = tk.Entry(self.canvas, width=30, bg=ENTRY_BG, fg=BUTTON_FG, font=FONT, highlightbackground=ENTRY_HIGHLIGHT, highlightthickness=2)
        self.submit_button = tk.Button(self.canvas, text="Enter", command=self.check_answer, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)
        self.score_label = tk.Label(self.canvas, text=f"Score: {self.score}", bg="#C38888", fg=THEME_FG, font=FONT)
        self.skip_button = tk.Button(self.canvas, text="Skip", command=self.skip_word, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)

        # Wizard animation elements (hidden initially)
        self.wizard_label = tk.Label(self.canvas, text="", bg="#C38888", fg=THEME_FG, font=FONT)
        self.wizard_images = []  # List to hold wizard animation frames (assume wizard1.png, wizard2.png, etc.)
        for i in range(1, 5):  # Assume 4 frames: wizard1.png to wizard4.png
            try:
                img = tk.PhotoImage(file=f'wizard.png{i}')
                self.wizard_images.append(img)
            except:
                self.wizard_images.append(None)
        self.animation_index = 0

    def load_high_score(self):
        if os.path.exists(self.high_score_file):
            with open(self.high_score_file, 'r') as f:
                try:
                    return int(f.read().strip())
                except:
                    return 0
        return 0

    def save_high_score(self):
        with open(self.high_score_file, 'w') as f:
            f.write(str(self.high_score))

    def get_lives_display(self):
        return "🍃" * self.lives

    def start_intro(self):
        # Hide intro elements
        self.intro_label.destroy()
        self.start_button.destroy()

        # Play intro sound (assume 'intro.mp3' exists)
        try:
            playsound('musics3.mp3')  # Play intro audio
        except Exception as e:
            print(f"Error playing intro sound: {e}")

        # Show game elements after a short delay
        self.root.after(3000, self.show_game_ui)  # Delay 3 seconds (adjust as needed)

    def show_game_ui(self):
        # Pack game UI elements on canvas
        self.canvas.create_window(300, 50, window=self.definition_label)
        self.canvas.create_window(300, 80, window=self.lives_label)
        self.canvas.create_window(300, 120, window=self.play_sound_button)
        self.canvas.create_window(300, 160, window=self.entry)
        self.canvas.create_window(300, 200, window=self.submit_button)
        self.canvas.create_window(300, 240, window=self.score_label)
        self.canvas.create_window(300, 280, window=self.skip_button)

        # Start the game
        self.start_game()

    def start_game(self):
        # Shuffle the words using random
        random.shuffle(self.words)

        # Select 10 random words from the 15
        selected_words = random.sample(self.words, 10)
        # Enqueue the selected words into the queue
        for word in selected_words:
            self.word_queue.enqueue(word)

        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.correct_words = []  # Reset correct words list
        self.all_inputs = []  # Reset all inputs list
        self.attempt_stack = Stack()  # Reset stack
        self.lives = 3  # Reset lives
        self.lives_label.config(text=f"Lives: {self.get_lives_display()}")
        self.getnext_Word()

    def getnext_Word(self):
        if not self.word_queue.is_empty() and self.lives > 0:
            self.current_word = self.word_queue.dequeue()
            self.definition_label.config(text=f"Definition: {self.current_word['definition']}")
            self.entry.delete(0, tk.END)  # Clear the textbox
        else:
            self.end_game()

    def play_sound(self):
        if self.current_word:
            try:
                playsound(self.current_word['audio'])  # Play the audio file, audio ra key
            except Exception as e:  # try catch exception, para d mata maw mag exit ket wat sueod ro music
                self.definition_label.config(text=f"Error playing sound: {e}")

    def check_answer(self):
        if self.current_word and self.lives > 0:
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
                self.root.after(2000, self.getnext_Word)  # Delay before next word
            else:
                self.lives -= 1  # Deduct life on wrong answer
                self.lives_label.config(text=f"Lives: {self.get_lives_display()}")
                if self.lives > 0:
                    self.definition_label.config(text=f"Incorrect. Try again! Lives left: {self.get_lives_display()}. Definition: {self.current_word['definition']}")
                else:
                    self.definition_label.config(text=f"Out of lives. The correct word is: {self.current_word['word']}. Definition: {self.current_word['definition']}")
                    self.end_game()

    def skip_word(self):
        if self.current_word and self.lives > 0:
            self.lives -= 1  # Deduct life on skip
            self.lives_label.config(text=f"Lives: {self.get_lives_display()}")
            if self.lives > 0:
                self.getnext_Word()
            else:
                self.end_game()

    def end_game(self):
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        # Check if perfect score (all 10 words correct)
        if self.score == 10:
            self.show_wizard_animation()
        else:
            # Show only high score
            self.definition_label.config(text=f"Game Over!\nYour Score: {self.score}\nHigh Score: {self.high_score}")
            self.play_sound_button.destroy()  # Remove playsound button
            self.entry.destroy()  # Remove textbox
            self.submit_button.destroy()  # Remove enter button
            self.lives_label.destroy()
            self.skip_button.config(text="Restart", command=self.replay_game)  # Replace with restart button

        # Optionally, review the stack (e.g., print the last attempt)
        if not self.attempt_stack.is_empty():
            last_attempt = self.attempt_stack.peek()  # Peek at the top of the stack
            print(f"Last attempt: Word '{last_attempt[0]}' was {'correct' if last_attempt[1] else 'incorrect'}")

        print(f"Final Score: {self.score} ")  # Console output for debugging

    def show_wizard_animation(self):
        # Hide other elements
        self.definition_label.config(text="Wow You're truly a wizard!")
        self.play_sound_button.destroy()
        self.entry.destroy()
        self.submit_button.destroy()
        self.lives_label.destroy()
        self.skip_button.destroy()

        # Show wizard label and start animation
        self.canvas.create_window(300, 200, window=self.wizard_label)
        self.animate_wizard()

    def animate_wizard(self):
        if self.wizard_images[self.animation_index]:
            self.wizard_label.config(image=self.wizard_images[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(self.wizard_images)
        self.root.after(500, self.animate_wizard)  # Animate every 500ms

    def replay_game(self):  # para mag uman
        # Recreate removed UI elements
        self.play_sound_button = tk.Button(self.canvas, text="Play Sound", command=self.play_sound, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)
        self.canvas.create_window(300, 120, window=self.play_sound_button)
        self.entry = tk.Entry(self.canvas, width=30, bg=ENTRY_BG, fg=BUTTON_FG, font=FONT, highlightbackground=ENTRY_HIGHLIGHT, highlightthickness=2)
        self.canvas.create_window(300, 160, window=self.entry)
        self.submit_button = tk.Button(self.canvas, text="Enter", command=self.check_answer, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT)
        self.canvas.create_window(300, 200, window=self.submit_button)
        self.lives_label = tk.Label(self.canvas, text=f"Lives: {self.get_lives_display()}", bg="#C38888", fg=THEME_FG, font=FONT)
        self.canvas.create_window(300, 80, window=self.lives_label)

        # Reset the game
        self.word_queue = Queue()  # Reset queue
        self.attempt_stack = Stack()  # Reset stack
        self.score = 0  # ibalik sa zero do score
        self.correct_words = []  # Reset correct words list
        self.all_inputs = []  # Reset all inputs list
        self.lives = 3  # Reset lives
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"Lives: {self.get_lives_display()}")
        self.definition_label.config(text="Definition will appear here.")
        self.skip_button.config(text="Skip", command=self.skip_word)  # Reset skip button
        self.start_game()  # kara euman nag uman it hampang

if __name__ == "__main__":
    root = tk.Tk()  # main window para kay tkinter
    game = SpellingGame(root)  # instantiate kuno
    root.mainloop()  # starts the Tkinter event loop