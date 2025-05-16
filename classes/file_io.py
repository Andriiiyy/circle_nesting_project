import re
from classes.circle import Circle


# === Зчитування кіл з текстового файлу ===
def load_circles_from_file(filename):
    circles = []
    pattern = r"Circle\s+\d+:\s+x=(\d+),\s*y=(\d+),\s*r=(\d+);"
    with open(filename, "r") as file:
        content = file.read()
        matches = re.findall(pattern, content)
        for i, (x, y, r) in enumerate(matches):
            circles.append(Circle(i, int(x), int(y), int(r)))
    return circles

