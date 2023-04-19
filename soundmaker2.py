import os
import shutil
import numpy as np
import soundfile as sf
from tkinter import Tk, filedialog, messagebox
from tkinter import Label
from tkinter import Button

class MainWindow:
    def __init__(self, master=None):
        self.master = master
        self.master.title('Spectral Resynthesis')
        self.master.geometry('400x150')
        self.input_folder_path = ''
        self.output_folder_path = os.path.join(os.path.expanduser('~'), 'Desktop')

        self.label = Label(self.master, text='Select a folder of WAV files to process:')
        self.label.place(x=10, y=10, width=380, height=40)

        self.select_button = Button(self.master, text='Select Folder', command=self.select_folder)
        self.select_button.place(x=10, y=60, width=120, height=30)

        self.process_button = Button(self.master, text='Process Files', command=self.process_files)
        self.process_button.place(x=150, y=60, width=120, height=30)
        self.process_button.config(state='disabled')

        self.quit_button = Button(self.master, text='Quit', command=self.quit)
        self.quit_button.place(x=290, y=60, width=90, height=30)

    def select_folder(self):
        self.input_folder_path = filedialog.askdirectory()
        if self.input_folder_path:
            self.process_button.config(state='normal')
            self.label.config(text=f'Selected folder: {self.input_folder_path}')
        else:
            self.process_button.config(state='disabled')
            self.label.config(text='Select a folder of WAV files to process:')

    def process_files(self):
        files = [f for f in os.listdir(self.input_folder_path) if f.endswith('.wav')]
        if not files:
            messagebox.showwarning('Warning', 'No WAV files found in selected folder.')
            return

        for file in files:
            file_path = os.path.join(self.input_folder_path, file)
            y, sr = sf.read(file_path)
            D = np.fft.rfft(y)
            S = np.abs(D)
            P = np.angle(D)
            S_resynth = np.random.uniform(0.2, 1.0, size=S.shape) * S
            D_resynth = S_resynth * np.exp(1j * P)
            y_resynth = np.fft.irfft(D_resynth)
            output_file_path = os.path.join(self.output_folder_path, f'resynth_{file}')
            sf.write(output_file_path, y_resynth, sr)

        messagebox.showinfo('Information', 'Processing complete.')
        self.label.config(text='Select a folder of WAV files to process:')
        self.process_button.config(state='disabled')

    def quit(self):
        self.master.destroy()

if __name__ == '__main__':
    root = Tk()
    window = MainWindow(root)
    window.master.mainloop()
