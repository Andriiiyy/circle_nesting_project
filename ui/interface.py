import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from time import perf_counter as timer

from classes.file_io import load_circles_from_file
from classes.circle_group import CircleGroup
from classes.circle import Circle
from utils.visualizer import visualize_circles_in_ui

def launch_interface():
    # === Ініціалізація вікна і стилів ===
    root = tk.Tk()
    root.title("Аналіз вкладеності кіл")
    root.geometry("1200x750")
    root.state('zoomed')
    style = ttk.Style(root)
    style.theme_use('classic')

    # === Глобальний стан програми ===
    app_state = {
        "group": CircleGroup([]),
        "highlight": []
    }

    # === Меню-бар ===
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Відкрити...", command=lambda: load_file())
    file_menu.add_separator()
    file_menu.add_command(label="Вийти", command=root.destroy)
    menubar.add_cascade(label="Файл", menu=file_menu)
    root.config(menu=menubar)

    # === Верхня панель ===
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(fill=tk.X)
    ttk.Label(top_frame, text="Завантажити файл:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
    entry_file = ttk.Entry(top_frame, width=50)
    entry_file.pack(side=tk.LEFT, padx=5)
    ttk.Button(top_frame, text="Огляд...", command=lambda: load_file()).pack(side=tk.LEFT, padx=5)

    ttk.Separator(root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

    # === Секція додавання кіл ===
    manual_frame = ttk.LabelFrame(root, text="Додати коло", padding=10)
    manual_frame.pack(fill=tk.X, padx=10, pady=5)
    ttk.Label(manual_frame, text="x:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
    entry_x = ttk.Entry(manual_frame, width=7); entry_x.grid(row=0, column=1, padx=5)
    ttk.Label(manual_frame, text="y:").grid(row=0, column=2, sticky=tk.W, padx=5)
    entry_y = ttk.Entry(manual_frame, width=7); entry_y.grid(row=0, column=3, padx=5)
    ttk.Label(manual_frame, text="r:").grid(row=0, column=4, sticky=tk.W, padx=5)
    entry_r = ttk.Entry(manual_frame, width=7); entry_r.grid(row=0, column=5, padx=5)
    ttk.Button(manual_frame, text="Додати вручну", command=lambda: add_manual_circle()).grid(row=0, column=6, padx=10)
    ttk.Button(manual_frame, text="Випадкове коло", command=lambda: add_random_circle()).grid(row=0, column=7, padx=5)

    ttk.Separator(root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

    # === Основна область: текст і графіка ===
    paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Ліва панель — текст
    text_frame = ttk.Frame(paned, width=400, relief=tk.GROOVE)
    paned.add(text_frame, weight=1)
    output_text = ScrolledText(text_frame, wrap=tk.WORD, font=('Consolas', 10))
    output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Права панель — візуалізація
    canvas_frame = ttk.Frame(paned, width=800, relief=tk.SUNKEN)
    paned.add(canvas_frame, weight=3)

    # === Функції обробки ===
    def load_file():
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not filename:
            return
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)
        circles = load_circles_from_file(filename)
        group = CircleGroup(circles)
        # Немає виклику старого build_nesting_tree(), алгоритми самі побудують
        app_state["group"] = group
        app_state["highlight"] = []
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Завантажено {len(circles)} кіл.\n")
        visualize_circles_in_ui(group, [], canvas_frame)

    def add_manual_circle():
        try:
            x, y, r = int(entry_x.get()), int(entry_y.get()), int(entry_r.get())
        except ValueError:
            messagebox.showerror("Помилка", "Введіть цілі числа для x, y, r.")
            return
        idx = len(app_state["group"].circles)
        c = Circle(idx, x, y, r)
        app_state["group"].circles.append(c)
        output_text.insert(tk.END, f"Додано коло #{idx}: x={x}, y={y}, r={r}\n")
        visualize_circles_in_ui(app_state["group"], [], canvas_frame)

    def add_random_circle():
        x, y, r = random.randint(0,1000), random.randint(0,1000), random.randint(5,100)
        idx = len(app_state["group"].circles)
        c = Circle(idx, x, y, r)
        app_state["group"].circles.append(c)
        output_text.insert(tk.END, f"Згенеровано коло #{idx}: x={x}, y={y}, r={r}\n")
        visualize_circles_in_ui(app_state["group"], [], canvas_frame)

    def run_algorithm1():
        output_text.delete("1.0", tk.END)
        start = timer()
        area, group = app_state["group"].find_largest_nested_group_dfs()
        elapsed = timer() - start
        app_state["highlight"] = group
        output_text.insert(tk.END,
            f"Алгоритм 1 (DFS)\n"
            f"Сумарна площа: {area:.2f}\n"
            f"Кількість кіл: {len(group)}\n"
            f"Час: {elapsed:.6f} с\n"
        )
        visualize_circles_in_ui(app_state["group"], group, canvas_frame)

    def run_algorithm2():
        output_text.delete("1.0", tk.END)
        start = timer()
        area, group = app_state["group"].find_largest_nested_group_kd()
        elapsed = timer() - start
        app_state["highlight"] = group
        output_text.insert(tk.END,
            f"Алгоритм 2 (KD-дерево)\n"
            f"Сумарна площа: {area:.2f}\n"
            f"Кількість кіл: {len(group)}\n"
            f"Час: {elapsed:.6f} с\n"
        )
        visualize_circles_in_ui(app_state["group"], group, canvas_frame)

    def save_image():
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG Image","*.png")])
        if path:
            visualize_circles_in_ui(app_state["group"],
                                    app_state.get("highlight", []),
                                    canvas_frame,
                                    save_path=path)
            messagebox.showinfo("Успіх", f"Зображення збережено: {path}")

    def clear_all():
        app_state["group"] = CircleGroup([])
        app_state["highlight"] = []
        output_text.delete("1.0", tk.END)
        visualize_circles_in_ui(app_state["group"], [], canvas_frame)

    # === Панель кнопок алгоритмів, збереження і очищення ===
    bottom_frame = ttk.Frame(root, padding=10)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    ttk.Button(bottom_frame, text="Алгоритм 1 (DFS)", command=run_algorithm1).pack(side=tk.LEFT, padx=10)
    ttk.Button(bottom_frame, text="Алгоритм 2 (KD-дерево)", command=run_algorithm2).pack(side=tk.LEFT, padx=10)
    ttk.Button(bottom_frame, text="Зберегти зображення", command=save_image).pack(side=tk.RIGHT, padx=10)
    ttk.Button(bottom_frame, text="Очистити", command=clear_all).pack(side=tk.RIGHT, padx=10)

    # Початкова візуалізація
    visualize_circles_in_ui(app_state["group"], [], canvas_frame)

    root.mainloop()
