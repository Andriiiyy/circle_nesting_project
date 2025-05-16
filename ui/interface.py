import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from time import time

from classes.file_io import load_circles_from_file
from classes.circle_group import CircleGroup
from utils.visualizer import visualize_circles_in_ui

def launch_interface():
    def load_file():
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            entry_file.delete(0, tk.END)
            entry_file.insert(0, filename)
            circles = load_circles_from_file(filename)
            group = CircleGroup(circles)
            group.build_nesting_tree()
            app_state["group"] = group
            app_state["highlight"] = []
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Файл завантажено. Всі вкладені кола показано синім кольором.\n")
            visualize_circles_in_ui(group, [], canvas_frame)

    def run_algorithm1():
        if "group" not in app_state:
            return
        output_text.delete("1.0", tk.END)
        start = time()
        area, group = app_state["group"].find_largest_nested_group()
        elapsed = time() - start
        app_state["highlight"] = group
        output_text.insert(tk.END, f"Алгоритм 1 (DFS)\nСумарна площа: {area:.2f}\nКількість вкладених кіл(червоних): {len(group)}\nЧас виконання: {elapsed:.4f} с\n")
        visualize_circles_in_ui(app_state["group"], group, canvas_frame)

    def run_algorithm2():
        if "group" not in app_state:
            return
        output_text.delete("1.0", tk.END)
        start = time()
        area, group = app_state["group"].find_largest_nested_group_dp()
        elapsed = time() - start
        app_state["highlight"] = group
        output_text.insert(tk.END, f"Алгоритм 2 (Динамічне програмування)\nСумарна площа: {area:.2f}\nКількість вкладених кіл(червоних): {len(group)}\nЧас виконання: {elapsed:.4f} с\n")
        visualize_circles_in_ui(app_state["group"], group, canvas_frame)

    def save_image():
        if "group" not in app_state:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if path:
            visualize_circles_in_ui(app_state["group"], app_state.get("highlight", []), canvas_frame, save_path=path)
            messagebox.showinfo("Успіх", f"Збережено у файл: {path}")

    # ==== Побудова UI ====
    root = tk.Tk()
    root.title("Аналіз вкладеності кіл")
    root.geometry("1200x700")
    app_state = {}

    # Верхній фрейм: вибір файлу, збереження
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)

    tk.Label(top_frame, text="Файл:").pack(side=tk.LEFT)
    entry_file = tk.Entry(top_frame, width=60)
    entry_file.pack(side=tk.LEFT, padx=5)
    tk.Button(top_frame, text="Огляд...", command=load_file).pack(side=tk.LEFT)
    tk.Button(top_frame, text="Зберегти зображення", command=save_image).pack(side=tk.LEFT, padx=5)

    # Головний фрейм
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Ліва частина (кнопки, текст)
    left_frame = tk.Frame(main_frame, width=600)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(left_frame)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Розв'язати за допомогою DFS", command=run_algorithm1).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Розв'язати методом динамічного програмування", command=run_algorithm2).pack(side=tk.LEFT, padx=5)

    output_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=30)
    output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Права частина (графіка)
    canvas_frame = tk.Frame(main_frame, bg="white", width=600)
    canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    root.mainloop()
