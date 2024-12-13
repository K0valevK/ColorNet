import itertools
import logging
from graphics.figure import Graphic, Rectangle, Triangle, Circle
from random import choice, choices, randint
from math import sqrt


logger = logging.getLogger(__name__)


def calc_dist(coord1: tuple[int, int], coord2: tuple[int, int]):
    return sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


class RoundGenerator:
    @classmethod
    def choose_colors(cls, color_count):
        return choices(["white", "red", "blue", "green", "yellow", "orange"], k=color_count)

    @classmethod
    def choose_shapes(cls, shape_count):
        return choices([Rectangle, Triangle, Circle], k=shape_count)

    @classmethod
    def create_question(cls, chosen_shapes, chosen_colors):
        question_type, question_color = None, None
        while question_color is None and question_type is None:
            question_type, question_color = choice(chosen_shapes), choice(chosen_colors)
        return question_type, question_color

    @classmethod
    def generate_answer(cls, figures, question_type, question_color):
        answer = 0
        if question_type is None:
            question_type = [Rectangle, Triangle, Circle]
        else:
            question_type = [question_type]
        if question_color is None:
            question_color = ["white", "red", "blue", "green", "yellow", "orange"]
        else:
            question_color = [question_color]
        for keys in list(itertools.product(question_type, question_color)):
            answer += len(figures[keys])
        return answer

    @classmethod
    def create_position(cls, existing_coords) -> tuple[int, int]:
        while True:
            flag = True
            x_pos = randint(100, 980)
            y_pos = randint(100, 420)
            for coords in existing_coords:
                if calc_dist((x_pos, y_pos), coords) < 100:
                    flag = False
                    break
            if flag:
                return x_pos, y_pos

    @classmethod
    def create_round(cls, shapes_count, colors_count, overall_count, same_size=False, same_color=False, same_speed=False, same_shape=False):
        chosen_colors = cls.choose_colors(colors_count)
        chosen_shapes = cls.choose_shapes(shapes_count)

        figure_colors = [choice(chosen_colors) if not same_color else chosen_colors[0] for _ in range(overall_count)]
        figure_size = [randint(30, 80) if not same_size else 40 for _ in range(overall_count)]
        figure_speed = [(float(randint(-2, 2)), float(randint(-2, 2))) if not same_speed else (1.0, 1.0) for _ in range(overall_count)]
        figure_types = [choice(chosen_shapes) if not same_shape else chosen_shapes[0] for _ in range(overall_count)]
        existing_coords = []
        figures = {}
        for i in range(overall_count):
            existing_coords.append(cls.create_position(existing_coords))
            figures.setdefault((figure_types[i], figure_colors[i]), []).append(
                Graphic(figure_types[i], *existing_coords[-1], figure_size[i], figure_colors[i], *figure_speed[i])
            )

        question_type, question_color = cls.create_question(chosen_shapes, chosen_colors)
        answer = cls.generate_answer(figures, question_type, question_color)
        logger.info("Created question %s %s with answer %d", question_color, question_type.to_str(), answer)

        return question_type, question_color, answer, [figure for row in figures.values() for figure in row]

