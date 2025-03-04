import matrix as mt


print("Welcome to matrix calculator!")

current_matrix = None
while True:
    print("Syntax:\n-init [dimension]\n-print\n-determinant\n-display_diagonal [main(0 or 1)]\n-make-triangular\n-exit")
    command = input(": ").split(" ")
    if len(command) > 2:
        print("Invalid syntax!")
        continue
    if command[0] == "-init":
        try:
            current_matrix = mt.init_matrix(int(command[1]))
        except Exception as e:
            print(e)
            continue
        mt.set_matrix_cin(current_matrix)
    elif command[0] == "-print":
        if current_matrix is None:
            print("No matrix set.")
            continue
        mt.print_matrix(current_matrix)
    elif command[0] == "-determinant":
        if current_matrix is None:
            print("No matrix set.")
            continue
        print(mt.determinant(current_matrix))
        print(f"Matrix singular: {mt.determinant(current_matrix) == 0}")

    elif command[0] == "-display_diagonal":
        if current_matrix is None:
            print("No matrix set.")
            continue
        try:
            mt.print_diagonal(current_matrix, bool(int(command[1])))
        except Exception as e:
            print(e)
            continue
    elif command[0] == "-make-triangular":
        if current_matrix is None:
            print("No matrix set.")
            continue
        mt.triangular_matrix(current_matrix)
    elif command[0] == "-exit":
        break