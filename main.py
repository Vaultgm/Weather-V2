import tkinter as tk
from tkinter import messagebox, Text
from PIL import Image, ImageTk
import requests
from datetime import datetime

def get_current_weather(city):
    api_key = "d5333f2d6478120a6bbb2ca1950eb380"  # Замените на ваш API ключ!!! Replace with your API key!!!
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(weather_url)

    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"Текущая температура: {temp}°C\nОписание: {description}"
    else:
        return "Не удалось получить данные о погоде."


def show_current_weather(event=None):
    city = city_entry.get()
    if city:
        weather_info = get_current_weather(city)
        result_label.config(text=weather_info)

        with open("weather_log.txt", "a") as file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Дата и время запроса: {current_time}\nГород: {city}\n{weather_info}\n\n")

        display_saved_weather()
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, введите название города")


def display_saved_weather():
    text_area.delete("1.0", tk.END)
    try:
        with open("weather_log.txt", "r") as file:
            saved_weather = file.read()
            text_area.insert(tk.END, saved_weather)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл сохраненных данных о погоде не найден.")


root = tk.Tk()
root.title("Погода")
root.geometry("900x1000")

try:
    image = Image.open("bg.png")
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Ошибка", f"Ошибка загрузки изображения: {e}")

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

city_entry = tk.Entry(frame, font=('Helvetica', 14, 'bold'), fg='#666666', justify='center')
city_entry.insert(0, 'Введите желаемый город')
city_entry.bind("<FocusIn>", lambda event: city_entry.delete(0, tk.END))
city_entry.bind("<FocusOut>", lambda event: city_entry.insert(0,
                                                              'Введите желаемый город'))
city_entry.place(relwidth=0.65, relheight=1)

search_button = tk.Button(frame, text="Показать погоду", font=('Helvetica', 12, 'bold'), fg='white', bg='#007BFF',
                          command=show_current_weather)
search_button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

result_label = tk.Label(lower_frame, font=('Helvetica', 14), anchor='center', justify='center', bd=4, bg='white',
                        fg='#333333', wraplength=300, padx=10, pady=10, relief='groove', borderwidth=2)
result_label.place(relwidth=1, relheight=0.5)

text_area = Text(lower_frame, font=('Helvetica', 10), wrap=tk.WORD)
text_area.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

root.mainloop()
