def init_matrix(dim: int) -> list[list[int]]:
    matrix = [[0] * dim for _ in range(dim)]
    return matrix
def print_matrix(matrix: list[list[int]]) -> None:
    for row in matrix:
        print(row)


def set_matrix_cin(matrix: list[list[int]]) -> None:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            readyToLeave = False
            while not readyToLeave:
                try:
                    matrix[i][j] = int(input(f"Now entering for position i: {i}, j: {j}: "))
                    readyToLeave = True
                except ValueError:
                    print("Value error!")

def submatrix(matrix: list[list[int]], i_exclude: int, j_exclude: int) -> list[list[int]]:
    new_matrix = init_matrix(len(matrix) - 1)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == i_exclude or j == j_exclude:
                continue
            i_norm = i
            if i > i_exclude:
                i_norm = i_norm - 1
            j_norm = j
            if j > j_exclude:
                j_norm = j_norm - 1
            new_matrix[i_norm][j_norm] = matrix[i][j]
    return new_matrix
def determinant(matrix: list[list[int]]) -> float:
    if len(matrix) == 1 and len(matrix[0]) == 1:
        return matrix[0][0]
    if len(matrix) == 2 and len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    determinant_value = 0.0
    for j in range(len(matrix[0])):
        submatrix_obj = submatrix(matrix, 0, j)
        if j % 2 == 0:
            determinant_value += matrix[0][j] * determinant(submatrix_obj)
        else:
            determinant_value += -1*matrix[0][j] * determinant(submatrix_obj)
    return determinant_value

def print_diagonal(matrix: list[list[int]], main_diagonal: bool) -> None:
    if main_diagonal:
        print("main")
        for i in range(len(matrix)):
            for j in range(i + 1):
                if i == j:
                    print(matrix[i][j], end=" ")
    else:
        print("additional")
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if i == len(matrix) - j - 1:
                    print(matrix[i][j], end=" ")
    print()


def triangular_matrix(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        pivot = i
        while pivot < n and matrix[pivot][i] == 0:
            pivot += 1
        if pivot == n:
            continue
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
        for j in range(i + 1, n):
            if matrix[j][i] != 0:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]