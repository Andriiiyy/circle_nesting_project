from classes.circle import Circle


class CircleGroup:
    def __init__(self, circles):
        self.circles = circles  # список усіх кіл
        self.roots = []         # кореневі елементи дерева вкладеності

    def build_nesting_tree(self):
        """Будує ієрархію вкладених кіл (дерево)"""
        sorted_circles = sorted(self.circles, key=lambda c: -c.r)  # від більшого до меншого
        for i, outer in enumerate(sorted_circles):
            for inner in sorted_circles[i+1:]:
                if inner.parent is None and inner.is_inside(outer):
                    outer.children.append(inner)
                    inner.parent = outer

        self.roots = [c for c in self.circles if c.parent is None]

    def find_largest_nested_group(self):
        """Знаходить групу вкладених кіл з найбільшою сумарною площею"""
        def dfs(circle):
            total_area = circle.area
            total_list = [circle]
            for child in circle.children:
                child_area, child_list = dfs(child)
                total_area += child_area
                total_list += child_list
            return total_area, total_list

        max_area = 0
        max_group = []

        for root in self.roots:
            area, group = dfs(root)
            if area > max_area:
                max_area = area
                max_group = group

        return max_area, max_group



    def find_largest_nested_group_dp(self):
        memo = {}

        def dp(circle):
            if circle in memo:
                return memo[circle]

            total_area = circle.area
            group = [circle]

            for child in circle.children:
                child_area, child_group = dp(child)
                total_area += child_area
                group += child_group

            memo[circle] = (total_area, group)
            return memo[circle]

        best_area = 0
        best_group = []

        for circle in self.circles:
            if circle.parent is None:  # запускати лише з кореневих вузлів
                area, group = dp(circle)
                if area > best_area:
                    best_area = area
                    best_group = group

        return best_area, best_group

