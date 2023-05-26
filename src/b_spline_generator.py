class Spline:
    def __init__(self, coefficients, horizontal_knots, spline_degree):
        self.degree = spline_degree  # Степень сплайна
        self.segments_number = len(horizontal_knots) - 2  # Количество сегментов
        self.coefficients = coefficients  # Коэффициенты сплайна
        horizontal_knots.sort()
        self.left_border = horizontal_knots[0]  # Левая граница сетки сплайна
        self.right_border = horizontal_knots[
            self.segments_number + 1
        ]  # Правая граница сетки сплайна
        self.enlarged_knots = (
            [self.left_border] * (self.degree + 1)
            + [0] * self.segments_number
            + [self.right_border] * (self.degree + 1)
        )  # Составим расширенный узловой вектор

        for i in range(self.segments_number):
            self.enlarged_knots[i + self.degree + 1] = horizontal_knots[i + 1]

    def get_degree(self):
        return self.degree

    def get_internal_knots_number(self):
        return self.segments_number

    def get_left_border(self):
        return self.left_border

    def get_right_border(self):
        return self.right_border

    # Вычисляем индекс заданного элемента в векторе узловых точек, начиная с заданного
    def get_point_index(self, point, min_id=0):
        if point < self.left_border or point > self.right_border:
            return -1

        while min_id < self.segments_number + self.degree and (
            self.enlarged_knots[min_id] > point
            or self.enlarged_knots[min_id + 1] <= point
        ):
            min_id += 1
        return min_id

    def b_splines(self, point, deg):
        left = self.get_point_index(point)
        vector_eng = [0] * (self.degree + 1)
        vector_eng[deg] = 1

        for right_index in range(1, deg + 1):
            v = left - right_index + 1
            w2 = (self.enlarged_knots[v + right_index] - point) / (
                self.enlarged_knots[v + right_index] - self.enlarged_knots[v]
            )
            vector_eng[deg - right_index] = w2 * vector_eng[deg - right_index + 1]
            for i in range(deg - right_index + 1, deg):
                w1 = w2
                v += 1
                w2 = (self.enlarged_knots[v + right_index] - point) / (
                    self.enlarged_knots[v + right_index] - self.enlarged_knots[v]
                )
                vector_eng[i] = (1 - w1) * vector_eng[i] + w2 * vector_eng[i + 1]
            vector_eng[deg] *= 1 - w2
        return vector_eng

    def get_value(self, point):
        point_index = self.get_point_index(point)
        vector_counter = [0] * (self.degree + 1)
        # Используем формулы Кокса Де Бура
        for i in range(self.degree + 1):
            vector_counter[i] = self.coefficients[i + point_index - self.degree]

        for j in range(1, self.degree + 1):
            for i in reversed(range(point_index - self.degree + j, point_index + 1)):
                count_coef = (point - self.enlarged_knots[i]) / (
                    self.enlarged_knots[i + 1 + self.degree - j]
                    - self.enlarged_knots[i]
                )
                vector_counter[i - point_index + self.degree] = (
                    count_coef * vector_counter[i - point_index + self.degree]
                    + (1 - count_coef)
                    * vector_counter[i - 1 - point_index + self.degree]
                )

        return vector_counter[self.degree]

    def get_knots(self):
        return self.enlarged_knots[self.degree : self.segments_number + self.degree + 2]

    def set_knots(self, horizontal_knots):
        horizontal_knots.sort()
        self.segments_number = len(horizontal_knots) - 2
        self.left_border = horizontal_knots[0]
        self.right_border = horizontal_knots[self.segments_number + 1]
        self.enlarged_knots = (
            [self.left_border] * (self.degree + 1)
            + [0] * self.segments_number
            + [self.right_border] * (self.degree + 1)
        )
        for i in range(self.segments_number):
            self.enlarged_knots[i + self.degree + 1] = horizontal_knots[i + 1]

    def set_coefficients(self, coefficients):
        self.coefficients = coefficients
