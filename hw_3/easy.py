import copy


class MatrixException(Exception):
    pass


class Matrix:
    def __init__(self, matrix):
        lines: int = len(matrix)
        columns: int = len(matrix[0])
        new_matrix = []
        for line in matrix:
            if len(line) != columns:
                raise MatrixException
            new_matrix.append([x for x in line])
        self.shape = (lines, columns)
        self.matrix = new_matrix

    def __add__(self, other):
        if self.shape != other.shape:
            raise MatrixException
        new_matrix = copy.deepcopy(self.matrix)
        other_shape = other.shape
        for i in range(other_shape[0]):
            for j in range(other_shape[1]):
                new_matrix[i][j] += other.matrix[i][j]
        return Matrix(new_matrix)

    def __mul__(self, other):
        if self.shape != other.shape:
            raise MatrixException
        new_matrix = copy.deepcopy(self.matrix)
        other_shape = other.shape
        for i in range(other_shape[0]):
            for j in range(other_shape[1]):
                new_matrix[i][j] *= other.matrix[i][j]
        return Matrix(new_matrix)

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise MatrixException
        result = [[0] * other.shape[1] for _ in range(self.shape[0])]
        shape = self.shape[0], other.shape[1]
        for i in range(shape[0]):
            for j in range(shape[1]):
                for r in range(self.shape[1]):
                    result[i][j] += self.matrix[i][r] * other.matrix[r][j]
        return Matrix(result)

    def __str__(self):
        return "[" + "\n".join([line.__str__() for line in self.matrix]) + "]"

    def __getitem__(self, item):
        return self.matrix[item]
