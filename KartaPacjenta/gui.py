import tkinter as tk
from tkinter import *
from tkinter import ttk

from main import Patient, PatientsDataLoader, Plot
from tkcalendar import Calendar, DateEntry
import datetime
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUI:
    def __init__(self, title, WIDTH, HEIGHT, RESIZABLE, patients):
        # Tworzenie okna
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(str(WIDTH) + "x" + str(HEIGHT))
        self.window.resizable(RESIZABLE, RESIZABLE)

        # do zapisania id obiektu z historii
        self.history_object_id = 0
        self.tmp_array = []
        self.block_new_info_window = False

        # Obiekt przechowujacy informacje o wszystkich pacjentach
        self.patientsData = patients

        # Zmienne
        self.filter_text_value = tk.StringVar()
        self.filter_text_value.set("")

        # Glowna ramka
        self.container = ttk.Frame(self.window)
        self.container.pack()

        self.table_name = ttk.Label(self.container, text="Filter by surname", font=25)
        self.table_name.pack(side=tk.TOP, anchor=tk.NW, pady=(20, 0))

        vcmd = (self.window.register(self.filterApplied),
                '%P')
        self.surname_filter_entry_text = tk.StringVar()
        self.surname_filter_entry_text.set('')

        self.surname_filter_entry = ttk.Entry(self.container, validate="key", validatecommand=vcmd, width=30,
                                              textvariable=self.surname_filter_entry_text)
        self.surname_filter_entry.pack(side=tk.TOP, anchor=tk.NW, pady=(5, 20))

        self.tree_scroll = tk.Scrollbar(self.container)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_view = ttk.Treeview(self.container, yscrollcommand=self.tree_scroll.set)

        # konfiguracja scrollbara
        self.tree_scroll.config(command=self.tree_view.yview)

        # Definicja kolumn
        self.tree_view['columns'] = ("Imie", "Nazwisko", "Plec", "Data urodzenia", "ID")

        # Defaultowa kolumna - nie potrzebujemy jej
        self.tree_view.column("#0", width=0)

        # Format kolumn
        self.tree_view.column("Imie", anchor=tk.W, width=100)
        self.tree_view.column("Nazwisko", anchor=tk.W, width=120)
        self.tree_view.column("Plec", anchor=tk.W, width=80)
        self.tree_view.column("Data urodzenia", anchor=tk.W, width=120)
        self.tree_view.column("ID", anchor=tk.W, width=280)

        # Nazwy kolumn
        self.tree_view.heading("Imie", text="Name", anchor=tk.CENTER)
        self.tree_view.heading("Nazwisko", text="Surname", anchor=tk.CENTER)
        self.tree_view.heading("Plec", text="Gender", anchor=tk.CENTER)
        self.tree_view.heading("Data urodzenia", text="Birth date", anchor=tk.CENTER)
        self.tree_view.heading("ID", text="Identifier", anchor=tk.CENTER)

        self.tree_view.pack(ipady=50)

        for patient in self.patientsData.patients:
            self.insertTable(patient)

        # Listener na klikniecia
        self.tree_view.bind("<Double-1>", self.onClickedRow)

        # Uruchamianie petli zdarzen
        self.window.mainloop()

    def filterApplied(self, input):
        if input == "":
            self.clearTable()
            print("GET ALL PATIENTS")
            for patient in self.patientsData.patients:
                self.insertTable(patient)
            return True
        patients_filtered = self.patientsData.getPatients_filtered(input)
        self.clearTable()
        print("GET PATIENTS WITH", input)
        for patient in patients_filtered:
            self.insertTable(patient)
        return True

    def insertTable(self, patient):
        # index='end' oznacza ze dodajemy na koniec tabeli
        self.tree_view.insert(parent='', index='end', iid=patient.id, text="",
                              values=(
                                  patient.name, patient.surname, patient.gender, patient.birth_date,
                                  patient.identifier))

    def clearTable(self):
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

    def onClickedRow(self, event):
        if self.block_new_info_window == False:
            item = self.tree_view.selection()[0]
            # Tutaj zamieszczamy informacje o pacjencie + edycja?
            print("Kliknieto: ", self.tree_view.item(item)['values'])
            self.block_new_info_window = True
            self.SpecificPatientWindow(self.patientsData.getPatient(self.tree_view.item(item)['values'][-1]))

    def SpecificPatientWindow(self, patient):

        self.form = tk.Toplevel(self.window)
        self.form.title("Dane pacjenta")
        self.form.geometry("1000x700")

        self.local_patient = patient

        # Zmienne
        self.name_text_value = tk.StringVar()
        self.name_text_value.set(patient.name)

        self.surname_text_value = tk.StringVar()
        self.surname_text_value.set(patient.surname)

        self.gender_text_value = tk.StringVar()
        self.gender_text_value.set(patient.gender)

        self.born_text_value = tk.StringVar()
        self.born_text_value.set(patient.birth_date)

        self.id_text_value = tk.StringVar()
        self.id_text_value.set(patient.id)

        self.identifier_text_value = tk.StringVar()
        self.identifier_text_value.set(patient.identifier)

        # Glowna ramka

        self.form_container = ttk.Frame(self.form)

        self.form_container.pack(fill=tk.BOTH, expand=True)

        self.card_title = ttk.Label(self.form_container, text="")
        self.card_title.grid(row=0, column=3, sticky=tk.W, pady=(20, 0), padx=5)

        self.margin_label = ttk.Label(self.form_container, textvariable='        ')
        self.margin_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.margin_label2 = ttk.Label(self.form_container, textvariable='        ')
        self.margin_label2.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)

        self.name_text_label = ttk.Label(self.form_container, textvariable=self.name_text_value)
        self.name_text_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

        self.surname_text_label = ttk.Label(self.form_container, textvariable=self.surname_text_value)
        self.surname_text_label.grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)

        self.gender_label = ttk.Label(self.form_container, text="Gender:")
        self.gender_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)

        self.gender_text_label = ttk.Label(self.form_container, textvariable=self.gender_text_value)
        self.gender_text_label.grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)

        self.id_label = ttk.Label(self.form_container, text="Identifier:")
        self.id_label.grid(row=1, column=3, sticky=tk.W, pady=5, padx=5)
        self.id_text_label = ttk.Label(self.form_container, textvariable=self.identifier_text_value)
        self.id_text_label.grid(row=1, column=4, sticky=tk.W, pady=5, padx=5)

        self.born_label = ttk.Label(self.form_container, text="Born:")
        self.born_label.grid(row=2, column=3, sticky=tk.W, pady=5, padx=5)
        self.born_text_label = ttk.Label(self.form_container, textvariable=self.born_text_value)
        self.born_text_label.grid(row=2, column=4, sticky=tk.W, pady=5, padx=5, columnspan=2)

        self.margin_label3 = ttk.Label(self.form_container, textvariable='        ')
        self.margin_label3.grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)

        self.start_date_label = ttk.Label(self.form_container, text="Start date:")
        self.start_date_label.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)

        self.start_date_entry = DateEntry(self.form_container, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=4, column=2, sticky=tk.W, pady=5, padx=5)

        begin_date = datetime.datetime(1990, 1, 1)
        end_date = datetime.datetime.now()

        self.end_date_label = ttk.Label(self.form_container, text="End date:")
        self.end_date_label.grid(row=4, column=3, sticky=tk.W, pady=5, padx=5)

        self.end_date_entry = DateEntry(self.form_container, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=4, column=4, sticky=tk.W, pady=5, padx=5)

        self.end_date_entry.set_date(end_date)
        self.start_date_entry.set_date(begin_date)

        self.history_filter_button = tk.Button(self.form_container, command=self.filterHistory, text="Filter history",
                                               bg="darkblue", fg="white")
        self.history_filter_button.grid(row=4, column=5, sticky=tk.W, pady=5, padx=5)

        style = ttk.Style()

        style.configure('myStyle1.Treeview', rowheight=48)

        self.history_tree_scroll = tk.Scrollbar(self.form_container)
        self.history_tree_scroll.grid(row=5, column=8, sticky='ns', pady=5, padx=5, rowspan=4)

        self.history_tree = ttk.Treeview(self.form_container, style='myStyle1.Treeview',
                                         yscrollcommand=self.history_tree_scroll.set)

        # konfiguracja scrollbara
        self.history_tree_scroll.config(command=self.history_tree.yview)

        # Definicja kolumn
        self.history_tree['columns'] = ("Date", "Type", "Info")

        # Defaultowa kolumna - nie potrzebujemy jej
        self.history_tree.column("#0", anchor=tk.W, width=80)

        self.med_img = tk.PhotoImage(file='medIMG.png')
        self.obs_img = tk.PhotoImage(file='obsIMG.png')

        self.history_tree.column("Date", anchor=tk.W, width=100)
        self.history_tree.column("Type", anchor=tk.W, width=80)
        self.history_tree.column("Info", anchor=tk.W, width=600)
        #  self.history_tree.column("Id", anchor=tk.W, width=0)

        self.history_tree.heading("Date", text="Date", anchor=tk.CENTER)
        self.history_tree.heading("Type", text="Type", anchor=tk.CENTER)
        self.history_tree.heading("Info", text="Info", anchor=tk.CENTER)

        self.history_tree.insert(parent='', index='end', iid=patient.id, text="")

        self.history_tree.grid(row=5, column=1, rowspan=3, columnspan=7, sticky=tk.W, pady=5, padx=5)

        self.plot_button = tk.Button(self.form_container,
                                     command=lambda arg=self.local_patient: self.showPlot(), text="Show plot",
                                     bg="darkblue", fg="white")
        self.plot_button.grid(row=4, column=6, sticky=tk.W, pady=5, padx=5)

        self.filterHistory()
        self.history_tree.tag_configure('odd', background='lightblue')
        self.history_tree.tag_configure('even', background='lightgrey')
        self.form.protocol("WM_DELETE_WINDOW", self.onClosing)

    def historyInsert(self, event, i):
        # index='end' oznacza ze dodajemy na koniec tabeli
        id = event['id']
        if event["type"] != 'medication':
            event_type = 'Observation'
            info = '[' + event['category'] + '] ' + event['name']
            img = self.obs_img

            if event['type'] == 'value':
                info += '\n' + str(event['value']) + ' ' + event['unit']
            elif event['type'] == 'values':
                info += '\n' + event['specific_name'][0] + ': ' + str(event['value'][0]) + ' ' + event['unit'][0] + '\n'
                info += event['specific_name'][1] + ': ' + str(event['value'][1]) + ' ' + event['unit'][1]
        else:
            event_type = 'Medication'
            info = event['name']
            img = self.med_img

        # to do wywalenia
        if i % 2 == 1:
            self.history_tree.insert(parent='', index='end', iid=event["id"], text="", image=img,
                                     values=(event["date"][:16].replace('T', '  '), event_type, info, id),
                                     tags=('odd',))
        else:
            self.history_tree.insert(parent='', index='end', iid=event["id"], text="", image=img,
                                     values=(event["date"][:16].replace('T', '  '), event_type, info, id),
                                     tags=('even',))

    def onClosing(self):
        self.block_new_info_window = False
        self.form.destroy()

    def clearHistoryTree(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

    def filterHistory(self):
        print("FILTER HISTORY")
        self.clearHistoryTree()
        for i, event in enumerate(self.local_patient.history_rangeLoader(str(self.start_date_entry.get_date()),
                                                                         str(self.end_date_entry.get_date()))):
            self.historyInsert(event, i)

    def showPlot(self):
        self.plot_button["state"] = "disabled"
        self.history_filter_button["state"] = "disabled"
        self.block_SpecificPatientWindow = True

        self.plot_window = tk.Toplevel(self.form)
        self.plot_window.title("Wykres")
        self.plot_window.geometry("800x500")

        self.radio_button_chosen = tk.IntVar()

        self.plot_container = ttk.Frame(self.plot_window)
        self.plot_container.pack(fill=tk.BOTH, expand=True)

        self.list_label = tk.Label(self.plot_container, text="Choose value:")
        self.list_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)

        self.drop_down_list = ttk.Combobox(self.plot_container,
                                           values=self.local_patient.observations_values_names)
        self.drop_down_list.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.drop_down_list.current(0)

        # self.drop_down_list.bind("<<ComboboxSelected>>", self.updatePlot)

        self.start_date_label_2 = tk.Label(self.plot_container, text="Choose start date:")
        self.start_date_label_2.grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)

        self.start_date_entry_2 = DateEntry(self.plot_container, width=12, background='darkblue',
                                            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry_2.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)

        self.update_plot_button = tk.Button(self.plot_container, command=self.updatePlot, text="Make plot",
                                            bg="darkblue", fg="white")
        self.update_plot_button.grid(row=6, column=5, sticky=tk.W, pady=5, padx=5)

        begin_date = datetime.datetime(1990, 1, 1)

        self.start_date_entry_2.set_date(begin_date)

        # Rysowanie wykresu
        self.plot = Plot()
        self.plot.create_plot(self.local_patient, self.drop_down_list.get(), str(self.start_date_entry_2.get_date()),
                              40000)
        self.canvas = FigureCanvasTkAgg(self.plot.fig, self.plot_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=7, columnspan=5)

        self.canvas._tkcanvas.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=7, columnspan=5)

        self.radio_label = tk.Label(self.plot_container, text="Duration:")
        self.radio_label.grid(row=0, column=5, sticky=tk.W, pady=0, padx=5)

        self.radio_button_1 = tk.Radiobutton(self.plot_container, text="half year", variable=self.radio_button_chosen,
                                             value=1)
        self.radio_button_1.grid(row=1, column=5, sticky=tk.W, pady=0, padx=5)

        self.radio_button_2 = tk.Radiobutton(self.plot_container, text="year", variable=self.radio_button_chosen,
                                             value=2)
        self.radio_button_2.grid(row=2, column=5, sticky=tk.W, pady=0, padx=5)

        self.radio_button_3 = tk.Radiobutton(self.plot_container, text="5 years", variable=self.radio_button_chosen,
                                             value=3)
        self.radio_button_3.grid(row=3, column=5, sticky=tk.W, pady=0, padx=5)

        self.radio_button_4 = tk.Radiobutton(self.plot_container, text="10 years", variable=self.radio_button_chosen,
                                             value=4)
        self.radio_button_4.grid(row=4, column=5, sticky=tk.W, pady=0, padx=5)

        self.radio_button_5 = tk.Radiobutton(self.plot_container, text="all", variable=self.radio_button_chosen,
                                             value=5)
        self.radio_button_5.grid(row=5, column=5, sticky=tk.W, pady=0, padx=5)
        # Default option - all
        self.radio_button_5.select()

        self.plot_window.protocol("WM_DELETE_WINDOW", self.closingPlot)

    def closingPlot(self):

        self.plot_button["state"] = "normal"
        self.history_filter_button["state"] = "normal"
        self.block_SpecificPatientWindow = False
        self.plot_window.destroy()

    def updatePlot(self):
        print("Combobox updated!")
        duration = 0
        val = self.radio_button_chosen.get()
        if val == 1:
            duration = 183
        elif val == 2:
            duration = 365
        elif val == 3:
            duration = 365 * 5 + 2
        elif val == 4:
            duration = 365 * 10 + 3
        elif val == 5:
            duration = 40000

        self.plot.create_plot(self.local_patient, self.drop_down_list.get(), str(self.start_date_entry_2.get_date()),
                              duration)

        self.plot_container.update()

        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=5, columnspan=5)

        self.canvas._tkcanvas.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=5, columnspan=5)
