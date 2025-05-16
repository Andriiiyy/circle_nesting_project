from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# === Візуалізація кіл в панелі UI ===
def visualize_circles_in_ui(group, highlight_group, container, save_path=None):
    # Очистити попередню графіку
    for widget in container.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.set_title("Графічне представлення кіл")


    # Якщо список кіл порожній — просто відобразимо порожній canvas
    if not group.circles:
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        return


    for circle in group.circles:
        if circle in highlight_group:
            color = "red"
        elif circle.parent is not None:
            color = "blue"
        else:
            color = "black"

        patch = plt.Circle((circle.x, circle.y), circle.r, edgecolor=color, fill=False, linewidth=1.5)
        ax.add_patch(patch)
        
    # Визначення меж
    min_x = min(c.x - c.r for c in group.circles)
    max_x = max(c.x + c.r for c in group.circles)
    min_y = min(c.y - c.r for c in group.circles)
    max_y = max(c.y + c.r for c in group.circles)
    ax.set_xlim(min_x - 10, max_x + 10)
    ax.set_ylim(min_y - 10, max_y + 10)
    #ax.grid(True)

    
    if save_path:
        fig.savefig(save_path)

    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)