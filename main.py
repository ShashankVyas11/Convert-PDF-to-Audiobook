import PyPDF2
from gtts import gTTS
import os
from tkinter import Tk, filedialog, Button, Label
import pygame

BACKGROUND='#FFFFFF'
YELLOW='#FFB627'
GRAY='#4A4A48'



# %%

class PDFToSpeechConverter:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDF to Speech Converter")
        self.root.config(bg=BACKGROUND)

        self.selected_file_label = Label(self.root, text="")
        self.selected_file_label.pack(pady=10)
        self.selected_file_label.config(bg=BACKGROUND,fg=GRAY)

        self.select_button = Button(self.root, text="Select PDF File", command=self.select_pdf_file)
        self.select_button.config(bg=GRAY, fg=YELLOW)
        self.select_button.pack(pady=10)

        self.play_button = Button(self.root, text="Play", state="disabled", command=self.play_audio)
        self.play_button.config(bg=GRAY, fg=YELLOW)
        self.play_button.pack(side="left", padx=10)
        self.pause_button = Button(self.root, text="Pause", state="disabled", command=self.pause_audio)
        self.pause_button.config(bg=GRAY, fg=YELLOW)
        self.pause_button.pack(side="left", padx=10)
        self.fast_forward_button = Button(self.root, text="Fast Forward", state="disabled", command=self.fast_forward_audio)
        self.fast_forward_button.config(bg=GRAY, fg=YELLOW)
        self.fast_forward_button.pack(side="left", padx=10)
        self.rewind_button = Button(self.root, text="Rewind", state="disabled", command=self.rewind_audio)
        self.rewind_button.config(bg=GRAY, fg=YELLOW)
        self.rewind_button.pack(side="left", padx=10)

        self.result_label = Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.file_path = None
        self.output_path = None
        self.audio_playing = False

    def select_pdf_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            self.selected_file_label.config(text=f"Selected Document: {os.path.basename(self.file_path)}")
            self.output_path = os.path.splitext(self.file_path)[0] + '_output.mp3'
            self.convert_pdf_to_speech()
            self.enable_audio_controls()

    def convert_pdf_to_speech(self):
        text = self.pdf_to_text(self.file_path)
        tts = self.text_to_speech(text)
        self.save_audio(tts, self.output_path)

    def pdf_to_text(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text

    def text_to_speech(self, text, language='en'):
        tts = gTTS(text=text, lang=language, slow=False)
        return tts

    def save_audio(self, tts, output_path):
        tts.save(output_path)

    def enable_audio_controls(self):
        self.play_button["state"] = "normal"
        self.pause_button["state"] = "normal"
        self.fast_forward_button["state"] = "normal"
        self.rewind_button["state"] = "normal"

    def play_audio(self):
        if not self.audio_playing:
            pygame.mixer.init()
            pygame.mixer.music.load(self.output_path)
            pygame.mixer.music.play()
            self.audio_playing = True

    def pause_audio(self):
        pygame.mixer.music.pause()
        self.audio_playing = False

    def fast_forward_audio(self):
        pygame.mixer.music.set_pos(min(pygame.mixer.music.get_pos() + 10, pygame.mixer.music.get_length()))

    def rewind_audio(self):
        pygame.mixer.music.set_pos(max(pygame.mixer.music.get_pos() - 10, 0))

    def run(self):
        self.root.mainloop()

# Create an instance of the PDFToSpeechConverter class
converter = PDFToSpeechConverter()
# Run the GUI application
converter.run()