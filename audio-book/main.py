import PyPDF2 as pdf
import pyttsx3 as tts
import customtkinter as ctk
import tkinter as tk
import threading

class PDFreader():
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')
        self.app = ctk.CTk()
        self.app.title("PDF reader")
        self.app.geometry("640x480")

        self.display = ctk.CTkFrame(self.app, height=260, width=620, fg_color='gray')
        self.display.place(x=10, y=0)

        self.text = ctk.CTkTextbox(master=self.display, height=260, width=620)
        self.text.pack(fill='both', expand=True)

        self.speak_btn = ctk.CTkButton(self.app, width=78, height=25, text='Read aloud', command=self.start_speaking)
        self.speak_btn.place(x=281, y=300)

        self.upload_button = ctk.CTkButton(self.app, width=78, height=25, text="Browse File", command=self.upload)
        self.upload_button.place(x=281, y=270)
        
        self.extracted_text = ""  # Variable to store extracted text
        
        self.app.mainloop()

    def upload(self):
        file_path = tk.filedialog.askopenfile(title='Select PDF', filetypes=[("PDF files", "*.pdf")])
        if file_path:
            # print(file_path)
            # Starting a new thread for processing the file
            threading.Thread(target=self.process, args=(file_path.name,)).start()

    def process(self, file_path):
        self.extracted_text = self.extract_text(file_path)
        self.display_frame(self.extracted_text)
        # self.start_speaking(data)

    def start_speaking(self):
        if self.extracted_text:
            # Starting a new thread for text-to-speech
            threading.Thread(target=self.say, args=(self.extracted_text,)).start()

    # This is used to start the engine and read the string it is passed 
    def say(self, command):
        engine = tts.init()
        engine.setProperty('rate', 160)
        engine.say(command)
        engine.runAndWait()

    def extract_text(self, path_to_pdf):
        # Extracts data from pdf file
        reader = pdf.PdfReader(path_to_pdf)

        # Displays metadata about the file
        # print(reader.metadata)

        # Displays the number of pages
        num_of_pages = len(reader.pages)
        # print(num_of_pages)

        # Extracts the text from pdf file from all the pages
        extracted_text = ""
        for num in range(num_of_pages):
            # print(num)
            page = reader.pages[num]
            extracted_text += page.extract_text() + '\n'
        return extracted_text.strip()

    def display_frame(self, text):
        # Use the `after` method to update the GUI from the main thread
        self.text.after(0, lambda: self.update_textbox(text))

    def update_textbox(self, text):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, text)

pdfread = PDFreader()