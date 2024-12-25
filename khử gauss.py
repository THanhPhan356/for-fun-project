# ...existing code...

def input_matrix():
    rows = int(input("Nhập số hàng của ma trận: "))
    cols = int(input("Nhập số cột của ma trận: "))
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            val = float(input(f"Nhập phần tử tại [{i}][{j}]: "))
            row.append(val)
        matrix.append(row)
    return matrix

def print_matrix(matrix):
    print("Ma trận hiện tại:")
    for row in matrix:
        print(" ".join(f"{elem:.2f}" for elem in row))

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for i in range(min(n, m)):
        # Tìm hàng có phần tử lớn nhất ở cột i
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        # Hoán đổi hàng
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Kiểm tra pivot
        if abs(matrix[i][i]) < 1e-12:
            print("Pivot bằng 0. Ma trận có thể suy biến.")
            continue

        # Khử tiến
        for k in range(i + 1, n):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, m):
                matrix[k][j] -= factor * matrix[i][j]

def main():
    matrix = input_matrix()
    print("\nMa trận ban đầu:")
    print_matrix(matrix)
    
    gaussian_elimination(matrix)
    
    print("\nMa trận sau khi khử Gauss:")
    print_matrix(matrix)

if __name__ == "__main__":
    main()
# ...existing code...