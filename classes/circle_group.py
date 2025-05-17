# classes/group.py

from scipy.spatial import KDTree
from classes.circle import Circle
import math

class CircleGroup:
    def __init__(self, circles):
        self.circles = circles
        self.roots = []

    def _reset_tree(self):
        """Очищаємо поля parent/children у всіх кіл"""
        for c in self.circles:
            c.parent = None
            c.children = []

    def build_nesting_tree(self):
        """
        Стандартна побудова дерева вкладеності через сортування за спаданням радіуса.
        """
        self._reset_tree()
        sorted_circles = sorted(self.circles, key=lambda c: -c.r)
        for i, outer in enumerate(sorted_circles):
            for inner in sorted_circles[i+1:]:
                if inner.parent is None and inner.is_inside(outer):
                    outer.children.append(inner)
                    inner.parent = outer
        self.roots = [c for c in self.circles if c.parent is None]

    def find_largest_nested_group_dfs(self):
        """
        Алгоритм 1: сортування за радіусом + DFS-пошук шляху з максимальною сумою площ.
        Повертає (max_area, list_of_circles_in_max_group).
        """
        # Спочатку будуємо дерево
        self.build_nesting_tree()

        def dfs(circle):
            total_area = circle.area
            total_chain = [circle]
            for child in circle.children:
                child_area, child_chain = dfs(child)
                total_area += child_area
                total_chain += child_chain
            return total_area, total_chain

        max_area = 0.0
        max_group = []
        for root in self.roots:
            area, group = dfs(root)
            if area > max_area:
                max_area = area
                max_group = group

        return max_area, max_group
    
    def find_largest_nestedgroup_kd(self):
        # Очищаємо попередні parent/children
        self._reset_tree()

        n = len(self.circles)
        if n == 0:
            return 0.0, []

        # Сортуємо за зростанням радіуса
        sorted_circles = sorted(self.circles, key=lambda c: c.r)
        points = [(c.x, c.y) for c in sorted_circles]
        tree = KDTree(points)

        max_radius = sorted_circles[-1].r

        # Знаходимо батьків для кожного кола
        parent = [None] * n
        for i, circle in enumerate(sorted_circles):
            # радіус пошуку — максимально можливий (різниця між max_radius та r_i)
            radius_search = max_radius - circle.r
            if radius_search <= 0:
                continue
            # шукаємо індекси всіх кіл у межах radius_search
            idxs = tree.query_ball_point(points[i], r=radius_search)
            # серед знайдених шукаємо найменший радіус батька, який вміщує це коло
            best_j = None
            best_r = math.inf
            for j in idxs:
                if j <= i:
                    continue
                candidate = sorted_circles[j]
                if candidate.r < best_r and candidate.is_inside(circle):
                    best_r = candidate.r
                    best_j = j
            if best_j is not None:
                parent[i] = best_j

        # Формуємо дерева children
        for i, p in enumerate(parent):
            if p is not None:
                sorted_circles[p].children.append(sorted_circles[i])
                sorted_circles[i].parent = sorted_circles[p]

        # Корені — ті, що без parent
        self.roots = [c for c in sorted_circles if c.parent is None]

        # Тепер DFS як у першому алгоритмі
        def dfs(circle):
            total_area = circle.area
            total_chain = [circle]
            for child in circle.children:
                child_area, child_chain = dfs(child)
                total_area += child_area
                total_chain += child_chain
            return total_area, total_chain

        max_area = 0.0
        max_group = []
        for root in self.roots:
            area, group = dfs(root)
            if area > max_area:
                max_area = area
                max_group = group


        return max_area, max_group











    def find_largest_nested_group_kd(self):
        """
        Алгоритм 2: KD-дерево для швидкого пошуку потенційних батьків + DFS.
        Повертає (max_area, list_of_circles_in_max_group).
        """

        self.build_nesting_tree()

        def kd(circle):
            total_area = circle.area
            total_chain = [circle]
            for child in circle.children:
                child_area, child_chain = kd(child)
                total_area += child_area
                total_chain += child_chain
            return total_area, total_chain

        max_area = 0.0
        max_group = []
        for root in self.roots:
            area, group = kd(root)
            if area > max_area:
                max_area = area
                max_group = group

        return max_area, max_group


        
