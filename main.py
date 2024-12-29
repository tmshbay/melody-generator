from pydub.generators import Sine
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def generate_note(frequency, duration_ms, amplitude=0.5):
    volume_db = -20 * (1 - amplitude)
    return Sine(frequency).to_audio_segment(duration=duration_ms, volume=volume_db)

def generate_harmonic_melody(duration_seconds=30, mood="happy", tempo=120, genre="classical"):
    """
    Создает гармоничную мелодию с заданной длительностью, настроением, темпом и жанром.
    """
    progressions = {
        "happy": [[261.63, 329.63, 392.00], [293.66, 349.23, 440.00], [329.63, 392.00, 493.88]],
        "sad": [[261.63, 311.13, 392.00], [293.66, 349.23, 415.30], [329.63, 392.00, 466.16]],
        "calm": [[261.63, 329.63, 392.00], [293.66, 349.23, 440.00], [261.63, 293.66, 349.23]],
    }

    rhythm_patterns = {
        "classical": [1, 0.5, 0.5, 2],
        "jazz": [0.5, 0.75, 0.75, 1],
        "pop": [1, 1, 0.5, 0.5, 1],
        "rock": [1, 0.5, 0.5, 1],
    }

    scale = progressions.get(mood, progressions["happy"])
    rhythm = rhythm_patterns.get(genre, rhythm_patterns["classical"])

    beats_per_second = tempo / 60
    beat_duration_ms = 1000 / beats_per_second
    total_duration_ms = 0
    target_duration_ms = duration_seconds * 1000

    melody = None
    while total_duration_ms < target_duration_ms:
        chord = random.choice(scale)
        for beat in rhythm:
            if total_duration_ms >= target_duration_ms:
                break
            duration_ms = int(beat * beat_duration_ms)
            frequency = random.choice(chord)
            note = generate_note(frequency, duration_ms)
            melody = note if melody is None else melody + note
            total_duration_ms += duration_ms

    return melody[:target_duration_ms]

def save_melody(melody, filename="melody.wav"):
    melody.export(filename, format="wav")
    messagebox.showinfo("Сохранение", f"Мелодия сохранена в файл {filename}")

def play_melody(melody):
    import simpleaudio as sa
    play_obj = sa.play_buffer(melody.raw_data, num_channels=1, bytes_per_sample=2, sample_rate=melody.frame_rate)
    play_obj.wait_done()

def create_ui():
    root = tk.Tk()
    root.title("Генератор мелодий")
    root.geometry("500x400")
    root.configure(bg="#1e1e2f")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", background="#6a0dad", foreground="#ffffff", font=("Helvetica", 10, "bold"))
    style.configure("TLabel", background="#1e1e2f", foreground="#ffffff", font=("Helvetica", 10))
    style.configure("TCombobox", selectbackground="#6a0dad", fieldbackground="#1e1e2f", foreground="#ffffff")

    header_frame = tk.Frame(root, bg="#6a0dad")
    header_frame.pack(fill="x", pady=10)
    header_label = tk.Label(header_frame, text="🎵 Добро пожаловать в Генератор Мелодий 🎵", bg="#6a0dad", fg="#ffffff", font=("Helvetica", 16, "bold"))
    header_label.pack()

    def generate_and_play():
        mood = mood_var.get()
        genre = genre_var.get()
        try:
            tempo = int(tempo_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Темп должен быть числом!")
            return

        melody = generate_harmonic_melody(duration_seconds=30, mood=mood, tempo=tempo, genre=genre)
        save_melody(melody, f"{genre}_{mood}_{tempo}_melody.wav")
        play_melody(melody)

    ttk.Label(root, text="Выберите настроение:").pack(pady=5, anchor="w", padx=20)
    mood_var = tk.StringVar(value="happy")
    mood_combobox = ttk.Combobox(root, textvariable=mood_var, values=["happy", "sad", "calm"], state="readonly")
    mood_combobox.pack(fill="x", padx=20, pady=5)

    ttk.Label(root, text="Выберите жанр:").pack(pady=5, anchor="w", padx=20)
    genre_var = tk.StringVar(value="classical")
    genre_combobox = ttk.Combobox(root, textvariable=genre_var, values=["classical", "jazz", "pop", "rock"], state="readonly")
    genre_combobox.pack(fill="x", padx=20, pady=5)

    ttk.Label(root, text="Темп (BPM):").pack(pady=5, anchor="w", padx=20)
    tempo_entry = ttk.Entry(root)
    tempo_entry.insert(0, "120")
    tempo_entry.pack(fill="x", padx=20, pady=5)

    generate_button = ttk.Button(root, text="Сгенерировать и воспроизвести", command=generate_and_play)
    generate_button.pack(pady=20, fill="x", padx=20)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
