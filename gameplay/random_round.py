from graphics.figure import Graphic, Rectangle
from random import choice, choices, randint
from math import sqrt


def calc_dist(coord1: tuple[int, int], coord2: tuple[int, int]):
    return sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


class RoundGenerator:
    @classmethod
    def choose_colors(cls, color_count):
        return choices(["white", "red", "blue", "green", "yellow", "orange"], k=color_count)

    @classmethod
    def create_question(cls, chosen_types, chosen_colors):
        return choice(chosen_types), choice(chosen_colors)

    @classmethod
    def create_position(cls, existing_coords) -> tuple[int, int]:
        while True:
            flag = True
            x_pos = randint(100, 620)
            y_pos = randint(100, 1180)
            for coords in existing_coords:
                if calc_dist((x_pos, y_pos), coords) < 100:
                    flag = False
                    break
            if flag:
                return x_pos, y_pos

    @classmethod
    def create_round(cls, types, colors_count, overall_count, same_size=False, same_color=False, same_speed=False):
        chosen_colors = cls.choose_colors(colors_count)

        figure_colors = [choice(chosen_colors) if not same_color else chosen_colors[0] for _ in range(overall_count)]
        figure_size = [randint(30, 80) if not same_size else 40 for _ in range(overall_count)]
        figure_types = [Rectangle for _ in range(overall_count)]
        existing_coords = []
        figures = {}
        for i in range(overall_count):
            existing_coords.append(cls.create_position(existing_coords))
            figures.setdefault((figure_types[i], figure_colors[i]), []).append(
                Graphic(figure_types[i], *existing_coords[-1], figure_colors[i])
            )

        question_type, question_color = cls.create_question([Rectangle], chosen_colors)
        answer = len(figures[question_type, question_color])

        return question_type, question_color, answer, [figure for row in figures.values() for figure in row]

