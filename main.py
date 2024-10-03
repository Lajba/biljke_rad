from tkinter import *
import sqlite3
import time
import datetime
import random
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

def prijava():
     unos_korisnik = Korisnik_entry.get()
     unos_lozinka = Lozinka_entry.get()
     conn = sqlite3.connect('Korisnici.db')
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM Korisnici WHERE Korisnik = ? AND Lozinka = ?", (unos_korisnik, unos_lozinka))
     user = cursor.fetchone()
     conn.close()

     if user:
          root.withdraw()
          glavni_izb = Toplevel()
          glavni_izb.title("Glavni izbornik")
          glavni_izb.geometry("1000x700")
          glavni_izb.config(bg="grey")
          background_image = Image.open(r'C:\Users\Wermacht\Desktop\Python\MOJI KODOVI\Labak zavrsni seminar\pozadina2.png')
          background_photo = ImageTk.PhotoImage(background_image)
          background_label = Label(glavni_izb, image=background_photo)
          background_label.place(relwidth=1, relheight=1)

          def update_time():
               current_time = time.strftime("%H:%M:%S")
               current_date = datetime.date.today().strftime("%d/%m/%Y")
               time_label.config(text=f"Vrijeme: {current_time}\nDatum: {current_date}")
               glavni_izb.after(1000, update_time)
############################################################################  KORISNICI
          def Korisnici():
               root_korisnici = Tk()
               root_korisnici.title("Korisnici")
               root_korisnici.geometry("800x500")
               root_korisnici.config(bg="#417255")
               korisnici_label = Label(root_korisnici, text="Korisnici",font='Helvetica 18 bold', bg="#417255")
               korisnici_label.place(relx=0.63, rely=0.07)
               kori_listbox = Listbox(root_korisnici, selectmode=SINGLE, width=40, height=20)
               kori_listbox.place(relx=0.1, rely=0.1)
               kori_label = Label(root_korisnici, text="ID ----- Ime ----- Prezime ----- Korisnik", bg="#417255")
               kori_label.place(relx=0.1, rely=0.05)
             
               def lista_korisnika():
                    kori_listbox.delete(0, END)
                    conn = sqlite3.connect('Korisnici.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id, Ime, Prezime, Korisnik FROM Korisnici")
                    korisnici = cursor.fetchall()
                    conn.close()

                    for k in korisnici:
                         lista_str = f"{k[0]} ----- {k[1]} ----- {k[2]} ----- {k[3]}"
                         kori_listbox.insert(END, lista_str)
           
               def dodaj_korisnika():
                    if user[5] == 1:
                         dodaj_k = Tk()
                         dodaj_k.title("Dodaj Korisnika")
                         dodaj_k.geometry("400x210")
                         dodaj_k.config(bg="#417255")

                         ime_label = Label(dodaj_k, text="Ime:", bg="#417255")
                         ime_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
                         ime_entry = Entry(dodaj_k)
                         ime_entry.grid(row=0, column=1, padx=10, pady=10)

                         prezime_label = Label(dodaj_k, text="Prezime:", bg="#417255")
                         prezime_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
                         prezime_entry = Entry(dodaj_k)
                         prezime_entry.grid(row=1, column=1, padx=10, pady=10)

                         korisnik_label = Label(dodaj_k, text="Korisnik:", bg="#417255")
                         korisnik_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
                         korisnik_entry = Entry(dodaj_k)
                         korisnik_entry.grid(row=2, column=1, padx=10, pady=10)

                         lozinka_label = Label(dodaj_k, text="Lozinka:", bg="#417255")
                         lozinka_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
                         lozinka_entry = Entry(dodaj_k, show="*")
                         lozinka_entry.grid(row=3, column=1, padx=10, pady=10)

                         role_label = Label(dodaj_k, text="Admin:", bg="#417255")
                         role_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
                         role_entry = Entry(dodaj_k)
                         role_entry.grid(row=4, column=1, padx=10, pady=10)
                         role_value_label = Label(dodaj_k, text="(1-DA / 0-NE)", bg="#417255")
                         role_value_label.grid(row=4, column=2, padx=10, pady=10, sticky="e")
                    
                         def dodaj_koris():
                              conn = sqlite3.connect('Korisnici.db')
                              cursor = conn.cursor()
                              cursor.execute("INSERT INTO Korisnici (Ime, Prezime, Korisnik, Lozinka, Role) VALUES (?, ?, ?, ?, ?)",
                                   (ime_entry.get(), prezime_entry.get(), korisnik_entry.get(), lozinka_entry.get(), role_entry.get()))
                              conn.commit()
                              conn.close()
                              lista_korisnika()  
                              dodaj_k.destroy()

                         dodaj_button = Button(dodaj_k, text="Dodaj", height=4, width=12, command=dodaj_koris)
                         dodaj_button.place(relx=0.65, rely=0.25)
                    else:
                              greska = Label(root_korisnici, text="Samo admin može dodati korisnika!", bg="#417255")
                              greska.place(relx=0.58, rely=0.75)
                              root_korisnici.after(2000, greska.destroy)
               
               def obrisi_korisnik():
                    selected_index = kori_listbox.curselection()
                    if selected_index:
                         selected_index = int(selected_index[0])
                         selected_user = kori_listbox.get(selected_index)
                    kori_id = selected_user.split("-----")[0].strip()
                    if user[5] == 1:
                         conn = sqlite3.connect('Korisnici.db')
                         cursor = conn.cursor()
                         cursor.execute("DELETE FROM Korisnici WHERE Id = ?", (kori_id,))
                         conn.commit()
                         conn.close()
                         lista_korisnika()
                    else:
                         greska = Label(root_korisnici, text="Samo admin može brisati korisnika!", bg="#417255")
                         greska.place(relx=0.58, rely=0.75)
                         root_korisnici.after(2000, greska.destroy)


               dodaj_korisnika_button = Button(root_korisnici, text="Dodaj Korisnika",height=5, width=17, command=dodaj_korisnika)
               dodaj_korisnika_button.place(relx=0.62, rely=0.25)   
               obrisi_korisnika_button = Button(root_korisnici, text="Obriši Korisnika", height=5, width=17, command=obrisi_korisnik)
               obrisi_korisnika_button.place(relx=0.62, rely=0.50)

               lista_korisnika()
               root_korisnici.mainloop()
################################################################################### BILJKE
          def Biljke():
               root_biljke = Tk()
               root_biljke.title("Biljke")
               root_biljke.geometry("800x500")
               root_biljke.config(bg="#417255")
               biljka_label = Label(root_biljke, text="Biljke",font='Helvetica 18 bold', bg="#417255")
               biljka_label.place(relx=0.65, rely=0.07)
               biljke_listbox = Listbox(root_biljke, selectmode=SINGLE, width=55, height=20)
               biljke_listbox.place(relx=0.05, rely=0.1)
               bilj_label = Label(root_biljke, text="ID ------ Ime ----- Temp ----- Vlaga ----- Svjetlost", bg="#417255")
               bilj_label.place(relx=0.05, rely=0.05)
          
               def lista_biljaka():
                    biljke_listbox.delete(0, END)
                    conn = sqlite3.connect('Biljke.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id, Ime, Temperatura, Vlaga, Svjetlost FROM Biljke")
                    biljke = cursor.fetchall()
                    conn.close()
                    for b in biljke:
                         lista_b = f"{b[0]} ----- {b[1]} ----- {b[2]} ----- {b[3]} ----- {b[4]}"
                         biljke_listbox.insert(END, lista_b)
               
               def dodaj_biljku():
                    dodaj_b = Tk()
                    dodaj_b.title("Dodaj Biljku")
                    dodaj_b.geometry("340x240")
                    dodaj_b.config(bg="#417255")

                    ime_biljke_label = Label(dodaj_b, text="Ime Biljke:", bg="#417255")
                    ime_biljke_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
                    ime_biljke_entry = Entry(dodaj_b)
                    ime_biljke_entry.grid(row=0, column=1, padx=10, pady=10)

                    temp_label = Label(dodaj_b, text="Temperatura:", bg="#417255")
                    temp_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
                    temp_entry = Entry(dodaj_b)
                    temp_entry.grid(row=1, column=1, padx=10, pady=10)
                    temp_value_label = Label(dodaj_b, text="(10 - 40)", bg="#417255")
                    temp_value_label.grid(row=1, column=3, padx=10, pady=10, sticky="e")
               
                    vlaga_label = Label(dodaj_b, text="Vlaga:", bg="#417255")
                    vlaga_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
                    vlaga_entry = Entry(dodaj_b)
                    vlaga_entry.grid(row=2, column=1, padx=10, pady=10)
                    vlaga_value_label = Label(dodaj_b, text="(10 - 40)", bg="#417255")
                    vlaga_value_label.grid(row=2, column=3, padx=10, pady=10, sticky="e")

                    svjetlost_label = Label(dodaj_b, text="Svjetlost:", bg="#417255")
                    svjetlost_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
                    svjetlost_entry = Entry(dodaj_b)
                    svjetlost_entry.grid(row=3, column=1, padx=10, pady=10)
                    svjetlost_value_label = Label(dodaj_b, text="(10 - 40)", bg="#417255")
                    svjetlost_value_label.grid(row=3, column=3, padx=10, pady=10, sticky="e")

                    def dodaj_biljku_db():
                         ime = ime_biljke_entry.get()
                         temperatura = temp_entry.get()
                         vlaga = vlaga_entry.get()
                         svjetlost = svjetlost_entry.get()
                         conn = sqlite3.connect('Biljke.db')
                         cursor = conn.cursor()
                         cursor.execute("INSERT INTO Biljke (Ime, Temperatura, Vlaga, Svjetlost) VALUES (?, ?, ?, ?)",
                                        (ime, temperatura, vlaga, svjetlost))
                         conn.commit()
                         conn.close()
                         lista_biljaka()
                         dodaj_b.destroy()

                    dodaj_bilj = Button(dodaj_b, text="Dodaj biljku", command=dodaj_biljku_db)
                    dodaj_bilj.grid(row=4, column=1, padx=10, pady=10)
               
               def obrisi_biljku():
                    selected_index = biljke_listbox.curselection()
                    if selected_index:
                         selected_index = int(selected_index[0])
                         selected_user = biljke_listbox.get(selected_index)
                    biljka_id = selected_user.split("-----")[0].strip()
                    if user[5] == 1:
                         conn = sqlite3.connect('Biljke.db')
                         cursor = conn.cursor()
                         cursor.execute("DELETE FROM Biljke WHERE Id = ?", (biljka_id,))
                         conn.commit()
                         conn.close()
                         lista_biljaka()
                    else:
                         greska = Label(root_biljke, text="Samo admin može brisati biljke!", bg="#417255")
                         greska.place(relx=0.59, rely=0.75)
                         root_biljke.after(2000, greska.destroy)

               dodaj_biljku_button = Button(root_biljke, text="Dodaj Biljku", height=5, width=17, command=dodaj_biljku)
               dodaj_biljku_button.place(relx=0.62, rely=0.25)
               obrisi_biljku_button = Button(root_biljke, text="Obriši Biljku", height=5, width=17, command=obrisi_biljku)
               obrisi_biljku_button.place(relx=0.62, rely=0.50)

               lista_biljaka()
               root_biljke.mainloop()
####################################################################### TEGLE
          def Tegle():
               root_tegle = Tk()
               root_tegle.title("Tegle")
               root_tegle.geometry("800x500")
               root_tegle.config(bg="#417255")
               tegle_label = Label(root_tegle, text="Tegle",font='Helvetica 18 bold', bg="#417255")
               tegle_label.place(relx=0.65, rely=0.07)
               tegla_listbox = Listbox(root_tegle, selectmode=SINGLE, width=40, height=20)
               tegla_listbox.place(relx=0.1, rely=0.1)
               tegla_label = Label(root_tegle, text="ID ----- Ime ----- Lokacija", bg="#417255")
               tegla_label.place(relx=0.1, rely=0.05)

               def lista_tegli():
                    tegla_listbox.delete(0, END)
                    conn = sqlite3.connect('Tegle.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id, Ime, Lokacija FROM Tegle")
                    tegla = cursor.fetchall()
                    conn.close()
                    for t in tegla:
                         lista_tegli = f"{t[0]} ----- {t[1]} ----- {t[2]}"
                         tegla_listbox.insert(END, lista_tegli)

               def dodaj_teglu():
                    dodaj_t = Tk()
                    dodaj_t.title("Dodaj Teglu")
                    dodaj_t.geometry("400x200")
                    dodaj_t.config(bg="#417255")

                    ime_label = Label(dodaj_t, text="Ime:", bg="#417255")
                    ime_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
                    ime_entry = Entry(dodaj_t)
                    ime_entry.grid(row=0, column=1, padx=10, pady=10)

                    Lokacija_label = Label(dodaj_t, text="Lokacija:", bg="#417255")
                    Lokacija_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
                    Lokacije = ["Kuhinja", "Dnevna", "Spavaca", "Balkon"]
                    selected_location = StringVar(dodaj_t)
                    selected_location.set(Lokacije[0])
                    lokacija_menu = OptionMenu(dodaj_t, selected_location, *Lokacije)
                    lokacija_menu.config(width=13)
                    lokacija_menu.grid(row=1, column=1, padx=10, pady=10)

                    def dodaj_teg():
                         selected_location_value = selected_location.get()
                         conn = sqlite3.connect('Tegle.db')
                         cursor = conn.cursor()
                         cursor.execute("INSERT INTO Tegle (Ime, Lokacija) VALUES (?, ?)",
                           (ime_entry.get(), selected_location_value))
                         conn.commit()
                         conn.close()
                         lista_tegla = f"{ime_entry.get()} ----- {selected_location_value}"
                         tegla_listbox.insert(END, lista_tegla)
                         lista_tegli()  
                         dodaj_t.destroy()

                    dodaj_button = Button(dodaj_t, text="Dodaj Teglu", height=4, width=12, command=dodaj_teg)
                    dodaj_button.place(relx=0.65, rely=0.25)

               def obrisi_teglu():
                    selected_index = tegla_listbox.curselection()
                    if selected_index:
                         selected_index = int(selected_index[0])
                         selected_user = tegla_listbox.get(selected_index)
                    tegla_id = selected_user.split("-----")[0].strip()
                    if user[5] == 1:
                         conn = sqlite3.connect('Tegle.db')
                         cursor = conn.cursor()
                         cursor.execute("DELETE FROM Tegle WHERE Id = ?", (tegla_id,))
                         conn.commit()
                         conn.close()
                         lista_tegli()
                    else:
                              greska = Label(root_tegle, text="Samo admin može brisati tegle!", bg="#417255")
                              greska.place(relx=0.59, rely=0.75)
                              root_tegle.after(2000, greska.destroy)
                 
               
               dodaj_teglu_button = Button(root_tegle, text="Dodaj Teglu",height=5, width=17, command=dodaj_teglu)
               dodaj_teglu_button.place(relx=0.62, rely=0.25)   
               obrisi_teglu_button = Button(root_tegle, text="Obriši Teglu", height=5, width=17, command=obrisi_teglu)
               obrisi_teglu_button.place(relx=0.62, rely=0.50)
             
               lista_tegli()
               root_tegle.mainloop()
############################################################## STATUS
          def Status():
               root_status = Tk()
               root_status.title("Status Biljaka")
               root_status.geometry("1000x700")
               root_status.config(bg="#417255")
               status_listbox = Listbox(root_status, selectmode=SINGLE, width=50, height=20)
               status_listbox.place(relx=0.1, rely=0.1)
               listbox_label = Label(root_status, text="ID ----- Ime ----- Temp ----- Vlaga ----- Svjetlost", bg="#417255")
               listbox_label.place(relx=0.1, rely=0.07)
               status_label = Label(root_status, text="Status", font='Helvetica 18 bold', bg="#417255")
               status_label.place(relx=0.65, rely=0.02)
               osijek_label = Label(root_status, text="Osijek:", font='Helvetica 14 bold', bg="#417255")
               osijek_label.place(relx=0.1, rely=0.73)
               historical_data = {}

               fig, ax_temp = plt.subplots(figsize=(5, 2))
               fig.suptitle("Temperatura Biljke")
               y_min, y_max = 10, 40
               ax_temp.set_ylim(y_min, y_max)
               ax_temp.set_yticks([10, 20, 30, 40])
               ax_temp.grid(True)
               canvas_temp = FigureCanvasTkAgg(fig, master=root_status)
               canvas_widget = canvas_temp.get_tk_widget()
               canvas_widget.place(relx=0.45, rely=0.08)

               fig, ax_humidity = plt.subplots(figsize=(5, 2))
               fig.suptitle("Vlaga Biljke")
               ax_humidity.set_ylim(10, 40)
               ax_humidity.set_yticks([10, 20, 30, 40])
               ax_humidity.grid(True)
               canvas_humidity = FigureCanvasTkAgg(fig, master=root_status)
               canvas_humidity_widget = canvas_humidity.get_tk_widget()
               canvas_humidity_widget.place(relx=0.45, rely=0.38)

               fig, ax_light = plt.subplots(figsize=(5, 2))
               fig.suptitle("Svjetlost Biljke")
               ax_light.set_ylim(10, 40)
               ax_light.set_yticks([10, 20, 30, 40])
               ax_light.grid(True)
               canvas_light = FigureCanvasTkAgg(fig, master=root_status)
               canvas_light_widget = canvas_light.get_tk_widget()
               canvas_light_widget.place(relx=0.45, rely=0.68)
             
               def lista_status():
                    conn = sqlite3.connect('Biljke.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id, Ime, Temperatura, Vlaga, Svjetlost FROM Biljke")
                    status = cursor.fetchall()
                    conn.close()

                    for s in status:
                         lista_status = f"{s[0]} ----- {s[1]} ----- {s[2]} ----- {s[3]} ----- {s[4]}"
                         status_listbox.insert(END, lista_status)

               def update_chart_from_listbox(event):
                    selected_item = status_listbox.get(status_listbox.curselection())
                    if selected_item:
                         selected_id = selected_item.split(" ----- ")[0]
                         update_chart(selected_id)
               status_listbox.bind('<<ListboxSelect>>', update_chart_from_listbox)
               
               def update_chart(selected_id):
                    if selected_id:
                         if selected_id in historical_data:
                              ax_temp.clear()
                              ax_humidity.clear()
                              ax_light.clear()
                              temperature_data = historical_data[selected_id]["Temperature"]
                              humidity_data = historical_data[selected_id]["Humidity"]
                              light_data = historical_data[selected_id]["Light"]
                              x_values = list(range(len(temperature_data)))
                              h_values = list(range(len(humidity_data)))
                              l_values = list(range(len(light_data)))
                              current_value_temp = temperature_data[-1]
                              current_value_humidity = humidity_data[-1]
                              current_value_light = light_data[-1]
                              ax_temp.plot(x_values, temperature_data, label="Temperatura")
                              ax_temp.scatter(len(temperature_data) - 1, current_value_temp, c='red', s=15, marker='o')
                              ax_humidity.plot(h_values, humidity_data, label="Vlaga")
                              ax_humidity.scatter(len(humidity_data) - 1, current_value_humidity, c='red', s=15, marker='o')
                              ax_light.plot(l_values, light_data, label="Svjetlost")
                              ax_light.scatter(len(light_data) - 1, current_value_light, c='red', s=15, marker='o')
               
                              for ax in [ax_temp, ax_humidity, ax_light]:
                                   ax.axhline(10, color='red', linestyle='--')
                                   ax.axhline(20, color='green', linestyle='--')
                                   ax.axhline(30, color='blue', linestyle='--')
                                   ax.axhline(40, color='purple', linestyle='--')
                                   ax.set_ylim(y_min, y_max)

                              ax_temp.set_xlim(0, len(temperature_data))
                              ax_temp.legend()
                              ax_humidity.set_xlim(0, len(humidity_data))
                              ax_humidity.legend()
                              ax_light.set_xlim(0, len(light_data))
                              ax_light.legend()

                              canvas_widget.place(relx=0.45, rely=0.08)
                              canvas_temp.draw()
                              canvas_humidity_widget.place(relx=0.45, rely=0.38)
                              canvas_humidity.draw()
                              canvas_light_widget.place(relx=0.45, rely=0.68)
                              canvas_light.draw()

               def update_status():
                    selected_index = status_listbox.curselection()
                    if selected_index:
                         selected_id = status_listbox.get(selected_index)[0].split(" ----- ")[0]
                         new_temperature = round(random.uniform(10, 40), 1)
                         new_humidity = round(random.uniform(10, 40), 1)
                         new_light = round(random.uniform(10, 40), 1)
                         if selected_id not in historical_data:
                              historical_data[selected_id] = {"Temperature": [], "Humidity": [], "Light": []}
                         historical_data[selected_id]["Temperature"].append(new_temperature)
                         historical_data[selected_id]["Humidity"].append(new_humidity)
                         historical_data[selected_id]["Light"].append(new_light)
                         conn = sqlite3.connect('Biljke.db')
                         cursor = conn.cursor()
                         cursor.execute("UPDATE Biljke SET Temperatura=?, Vlaga=?, Svjetlost=? WHERE Id=?", (new_temperature, new_humidity, new_light, selected_id))
                         conn.commit()
                         conn.close()
                         status_listbox.delete(0, END)
                         lista_status()
                         status_listbox.selection_set(selected_index)
                         success_label = Label(root_status, text="Status biljke se uspješno osvježilo!", bg="#417255")
                         success_label.place(relx=0.16, rely=0.67)
                         root_status.after(2000, success_label.destroy)
                         update_chart(selected_id)
                         

               def get_weather_data(api_key, city_id):  
                    api_url = "http://api.openweathermap.org/data/2.5/weather"  
                    params = {  
                              "id": city_id,  
                              "units": "metric",  
                              "appid": api_key  
                    }  
                    response = requests.get(api_url, params=params)  
                    data = response.json()  
                    return data
               
               api_key = "c94a2499bf7fc730cc0e2d7777112526"  
               city_id = "3193935"  # Osijek
               info = get_weather_data(api_key, city_id)  
               temperature = info["main"]["temp"]  
               humidity = info["main"]["humidity"]  
               pressure = info["main"]["pressure"]
                    
               sync_button = Button(root_status, text="Sync", height=2, width=15, command=update_status)
               sync_button.place(relx=0.19, rely=0.60)
               temp_label = Label(root_status, text=f"Temperatura: {round(temperature)}°C", font='Helvetica 12 bold', bg="#417255")
               temp_label.place(relx=0.13, rely=0.78)
               vlaga_label = Label(root_status,text=f"Vlaga: {round(humidity)}%", font='Helvetica 12 bold', bg="#417255")
               vlaga_label.place(relx=0.13, rely=0.83)
               tlak_label = Label(root_status,text=f"Tlak: {round(pressure)} hPa", font='Helvetica 12 bold', bg="#417255")
               tlak_label.place(relx=0.13, rely=0.88)
               
               root_status.after(0, get_weather_data)
               lista_status()
               root_status.mainloop()    
############################################## Spajanje
          def Spajanje():
               root_spajanje = Tk()
               root_spajanje.title("Spajanje Biljaka sa Teglama")
               root_spajanje.geometry("800x500")
               root_spajanje.config(bg="#417255")

               biljka_listbox = Listbox(root_spajanje, exportselection=0, width=30, height=20)
               biljka_listbox.place(relx=0.1, rely=0.1)
               biljka_label = Label(root_spajanje, text="ID ----- Biljka", bg="#417255")
               biljka_label.place(relx=0.1, rely=0.05)

               tegla_listbox = Listbox(root_spajanje, exportselection=0, width=30, height=20)
               tegla_listbox.place(relx=0.4, rely=0.1)
               tegla_label = Label(root_spajanje, text="ID ----- Tegla ----- Lokacija", bg="#417255")
               tegla_label.place(relx=0.4, rely=0.05)

               spajanje_listbox = Listbox(root_spajanje, selectmode=SINGLE, width=30, height=20)
               spajanje_listbox.place(relx=0.7, rely=0.1)
               spajanje_label = Label(root_spajanje, text="Biljka ID ----- Tegla ID", bg="#417255")
               spajanje_label.place(relx=0.7, rely=0.05)

               def biljke_box():
                    biljka_listbox.delete(0, END)
                    conn = sqlite3.connect('Biljke.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id, Ime FROM Biljke")
                    biljke = cursor.fetchall()
                    conn.close()
                    for b in biljke:
                         lista_b = f"{b[0]} ----- {b[1]}"
                         biljka_listbox.insert(END, lista_b)
               
               def tegla_box():
                    tegla_listbox.delete(0, END)
                    conn = sqlite3.connect('Tegle.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id, Ime, Lokacija FROM Tegle")
                    tegla = cursor.fetchall()
                    conn.close()
                    for t in tegla:
                         lista_tegli = f"{t[0]} ----- {t[1]} ----- {t[2]}"
                         tegla_listbox.insert(END, lista_tegli)

               def spajanje_box():
                    spajanje_listbox.delete(0, END)
                    conn = sqlite3.connect('Spajanje.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id, Biljka_id, Tegla_id FROM Spajanje")
                    spajanje = cursor.fetchall()
                    conn.close()
                    for s in spajanje:
                         lista_s = f"{s[1]} ----- {s[2]}"
                         spajanje_listbox.insert(END, lista_s)

               def spoji():
                    selected_biljka_index = biljka_listbox.curselection()
                    selected_tegla_index = tegla_listbox.curselection()
                    if selected_biljka_index and selected_tegla_index:
                         selected_biljka = biljka_listbox.get(selected_biljka_index[0])
                         selected_tegla = tegla_listbox.get(selected_tegla_index[0])
                         biljka_id = selected_biljka.split(" ----- ")[0]
                         tegla_id = selected_tegla.split(" ----- ")[0]
                         conn = sqlite3.connect('Spajanje.db')
                         cursor = conn.cursor()
                         cursor.execute("SELECT COUNT(*) FROM Spajanje WHERE Biljka_id = ? OR Tegla_id = ?", (biljka_id, tegla_id))
                         count = cursor.fetchone()[0]
                         if count == 0:
                              cursor.execute("INSERT INTO Spajanje (Biljka_id, Tegla_id) VALUES (?, ?)", (biljka_id, tegla_id))
                              conn.commit()
                              spajanje_listbox.insert(END, f"{biljka_id} ----- {tegla_id}")
                         else:
                              greska = Label(root_spajanje, text="Tegla ili Biljka je zauzeta", bg="#417255")
                              greska.place(relx=0.735, rely=0.9)
                              root_spajanje.after(2000, greska.destroy)
                         conn.close()

               def obrisi():
                    selected_spajanje_index = spajanje_listbox.curselection()
                    if selected_spajanje_index:
                         selected_spajanje = spajanje_listbox.get(selected_spajanje_index[0])
                         biljka_id, tegla_id = selected_spajanje.split(" ----- ")
                         conn = sqlite3.connect('Spajanje.db')
                         cursor = conn.cursor()
                         cursor.execute("DELETE FROM Spajanje WHERE Biljka_id = ? AND Tegla_id = ?", (biljka_id, tegla_id))
                         conn.commit()
                         conn.close()
                         spajanje_listbox.delete(selected_spajanje_index)
                         
               obrisi_button = Button(root_spajanje, text="Obriši", height=2, width=20, command=obrisi)
               obrisi_button.place(relx=0.725, rely=0.80)   
               spoji_button = Button(root_spajanje, text="Spoji", height=2, width=20, command=spoji)
               spoji_button.place(relx=0.425, rely=0.80)

               biljke_box()
               tegla_box()
               spajanje_box()          
               root_spajanje.mainloop()

          Status_button = Button(glavni_izb, text="Status Biljaka", height= 5, width=15, font=10, command=Status)
          Status_button.place(relx=0.35, rely=0.30, anchor=CENTER)
          Korisnici_button = Button(glavni_izb, text="Korisnici", height= 5, width=15, font=10, command=Korisnici)
          Korisnici_button.place(relx=0.20, rely=0.66, anchor=CENTER)
          Biljke_button = Button(glavni_izb, text="Biljke", height= 5, width=15, font=10, command=Biljke)
          Biljke_button.place(relx=0.5, rely=0.66, anchor=CENTER)
          Tegle_button = Button(glavni_izb, text="Tegle", height= 5, width=15, font=10, command=Tegle)
          Tegle_button.place(relx=0.80, rely=0.66, anchor=CENTER)
          Spajanje_button = Button(glavni_izb, text="Spajanje B-T", height= 5, width=15, font=10, command=Spajanje)
          Spajanje_button.place(relx=0.65, rely=0.30, anchor=CENTER)
          time_label = Label(glavni_izb, font=5)
          time_label.place(relx=1, rely=0, anchor="ne")
        
          update_time()
          glavni_izb.mainloop()
     else:
          error_label = Label(root, text="Korisnik ili Lozinka krivo unešena!")
          error_label.place(relx=0.5, rely=0.8, anchor=CENTER)

##### POCETNI LOGIN #####
root = Tk()
root.title("Prijava")
root.geometry("500x300")
root.config(bg="grey")

background_image = Image.open(r'C:\Users\Wermacht\Desktop\Python\MOJI KODOVI\Labak zavrsni seminar\pozadina.png')
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(root, image=background_photo)  
background_label.place(relwidth=1, relheight=1, relx=0, rely=0, anchor="nw")

Prijava_label = Label(root, text="PRIJAVA", font=20)
Prijava_label.place(relx=0.5, rely=0.2, anchor=CENTER)
Prijava_button = Button(root, text="Prijava", width=7, command=prijava)
Prijava_button.place(relx=0.5, rely=0.65, anchor=CENTER) 

Korisnik_label = Label(root, text="Korisnik:")
Korisnik_label.place(relx=0.3, rely=0.4,anchor=CENTER)    
Korisnik_entry = Entry(root)
Korisnik_entry.place(relx=0.5, rely=0.4, anchor=CENTER)
  
Lozinka_label = Label(root, text="Lozinka:")
Lozinka_label.place(relx=0.3, rely=0.5, anchor=CENTER) 
Lozinka_entry = Entry(root, show="*")
Lozinka_entry.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()
########################## KRAJ KODA

#### TABLICE SQL #####

### KORISNICI ###
conn1 = sqlite3.connect('Korisnici.db')
cursor1 = conn1.cursor()
cursor1.execute('''CREATE TABLE IF NOT EXISTS Korisnici (
                    Id INTEGER PRIMARY KEY,
                    Ime TEXT,
                    Prezime TEXT,
                    Korisnik TEXT,
                    Lozinka TEXT,
                    Role INTEGER,
                    )''')
conn1.commit()
conn1.close()

### BILJKA ###
conn2 = sqlite3.connect('Biljke.db')
cursor2 = conn2.cursor()
cursor2.execute('''CREATE TABLE IF NOT EXISTS Biljke (
                    Id INTEGER PRIMARY KEY,
                    Ime TEXT,
                    Temperatura REAL,
                    Vlaga REAL,
                    Svjetlost REAL
                    )''')
conn2.commit()
conn2.close()

### Tegle ###
conn3 = sqlite3.connect("Tegle.db")
cursor3 = conn3.cursor()
cursor3.execute('''CREATE TABLE IF NOT EXISTS Tegle (
    Id INTEGER PRIMARY KEY,
    Ime TEXT,            
    Lokacija TEXT CHECK (Lokacija IN ("Kuhinja", "Dnevna", "Spavaca", "Balkon"))
);''')
conn3.commit()
conn3.close()

### SPAJANJE ###
conn4 = sqlite3.connect("Spajanje.db")
cursor4 = conn4.cursor()
cursor4.execute('''CREATE TABLE IF NOT EXISTS Spajanje (
    ID INTEGER PRIMARY KEY,
    Biljka_id INTEGER,
    Tegla_id INTEGER
);''')
conn4.commit()
conn4.close()




