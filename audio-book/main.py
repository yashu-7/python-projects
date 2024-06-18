import PyPDF2 as pdf
import pyttsx3 as tts

# This is used to start the engine and read the string it is passed 
def say(command):
    engine = tts.init()
    engine.setProperty('rate',160)
    engine.say(command)
    engine.runAndWait()

# Path to the pdf file
text_book = "C:\\Users\\yaswa\\Downloads\\Meeting Agenda.pdf"

def extract_text_and_read(path_to_pdf):
    # Extracts data from pdf file
    reader = pdf.PdfReader(path_to_pdf) 

    # Displays metadata about the file
    # print(reader.metadata) 

    # Displays the number of pages
    num_of_pages = len(reader.pages)
    # print(num_of_pages) 

    # Extracts the text from pdf file from all the pages
    for num in range(num_of_pages):
        # print(num)
        page = reader.pages[num]
        data = page.extract_text()
        print(data)
        say(data)
        
extract_text_and_read(text_book)