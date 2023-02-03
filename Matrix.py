class Matrix:
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.dim = (rows, cols)
        if data:
            self.data = data
        else:
            self.data = [[0 for i in range(cols)] for j in range(rows)]
    
    def __str__(self):
        s = ''
        for row in self.data:
            s += ' '.join(map(str, row))
            s += '\n'
        return s

    def __getitem__(self, key):
        row, col = key
        return self.data[row][col]
    
    def __setitem__(self, key, value):
        row, col = key
        self.data[row][col] = value

    def __add__(self, other):
        if self.dim == other.dim:
            result = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    result[i, j] = self[i, j] + other[i, j]
            return result
        else:
            return NotImplemented

    def __sub__(self, other):
        if self.rows == other.rows and self.cols == other.cols:
            result = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    result[i, j] = self[i, j] - other[i, j]
            return result
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(self, Matrix) and isinstance(other, Matrix):
            if self.cols == other.rows:
                result = Matrix(self.rows, other.cols)
                for i in range(self.rows):
                    for j in range(other.cols):
                        for k in range(other.rows):
                            result[i, j] += self[i, k] * other[k, j]
                return result
            else:
                return NotImplemented
        if (isinstance(self, Matrix) and isinstance(other, int)) or (isinstance(self, Matrix) and isinstance(other, float)):
            result = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                    for j in range(self.cols):
                        result[i, j] = self[i, j] * other
            return result
        if isinstance(self, Matrix) and isinstance(other, Vector):
            if self.cols == other.size:
                result = Vector(other.size)
                for i in range(self.rows):
                    for j in range(other.size):
                            result[i] += self[i, j] * other[j]
                return result
            else:
                return NotImplemented
    
    def __pow__(self, power):
        if power == 0:
            return Matrix.identity_matrix(self.rows)
        elif power == -1:
            return self.inverse()
        else:
            result = self
            for i in range(power-1):
                result = result * self
            return result
    
    def identity_matrix(size):
        I = Matrix(size, size)
        for i in range(size):
            for j in range(size):
                if i == j:
                    I.data[i][j] = 1
        return I

    def binary_matrix(bits):
        M = Matrix(bits, bits)
        for i in range(bits):
            for j in range(bits):
                if i == j:
                    M.data[i][j] = 2 ** (i)
        return M

    def inverse(self):
        if self.rows == self.cols and self.det() != 0:
            adj = self.adjoint()
            inv = [[adj[i][j]/self.det() for j in range(len(adj))] for i in range(len(adj))]
            return inv
        else:
            return NotImplemented

    def swap_rows(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
    
    def multiply_row(self, i, scalar):
        self.data[i] = [scalar * x for x in self.data[i]]
    
    def add_multiple_of_row(self, i, j, scalar):
        self.data[i] = [a + scalar * b for a, b in zip(self.data[i], self.data[j])]
    
    def delete_row(self, row):
        result = Matrix(self.rows-1, self.cols)
        current_row = 0
        for i in range(self.rows):
            if i == row:
                continue
            for j in range(self.cols):
                result.data[current_row][j] = self.data[i][j]
            current_row += 1
        return result
    
    def delete_column(self, col):
        result = Matrix(self.rows, self.cols-1)
        current_col = 0
        for i in range(self.cols):
            if i == col:
                continue
            for j in range(self.rows):
                result.data[j][current_col] = self.data[j][i]
            current_col += 1
        return result
    
    def transpose(self):
        if isinstance(self, Matrix):
            result = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[j][i]
            return result
        if isinstance(self, Vector):
            result = Matrix(1, self.size)
            for i in range(self.size):
                result.data[0][i] = self.data[i]
            return result
    
    def getMatrixMinor(self,i,j):
        return [row[j] + row[j+1] for row in (self.data[i]+self.data[i+1])]
    
    def adjoint(self):
        cofactors = []
        for r in range(self.rows):
            cofactorRow = []
            for c in range(self.cols):
                minor = Matrix.getMatrixMinor(self,r,c)
                cofactorRow.append(((-1)**(r+c)) * minor.det())
                cofactors.append(cofactorRow)
        result = Matrix(len(cofactors), len(cofactors[0]))
        return result.transpose()

    def det(self):
        if self.rows == self.cols:
            if self.dim == (1, 1):
                determinant = self.data[0][0]
                return determinant
            elif self.dim == (2, 2):
                determinant = (self.data[0][0] * self.data[1][1]) - (self.data[0][1] * self.data[1][0])
                return determinant
            else:
                determinant = 0
                for i in range(self.cols):
                    submatrix = self.delete_row(0).delete_column(i)
                    determinant += (-1) ** i * self.data[0][i] * submatrix.det()
                return determinant  
        else:
            return NotImplemented    
    
    def rref(self):
        lead = 0
        row_count = self.rows
        col_count = self.cols
        
        for r in range(row_count):
            if lead >= col_count:
                return
            
            i = r
            while self.data[i][lead] == 0:
                i += 1
                if i == row_count:
                    i = r
                    lead += 1
                    if col_count == lead:
                        return
            
            self.swap_rows(i, r)
            self.multiply

    def eigenvalues(self):
        n = self.rows
        I = Matrix.identity_matrix(n)
        eigenvalues = []

        return eigenvalues
        
class Vector(Matrix):
    def __init__(self, size, data=None):
        super().__init__(size, 1)
        if data:
            self.data = data
        else:
            self.data = [[0 for i in range(1)] for j in range(size)]
        self.size = size

    def __iter__(self):
        for row in range(self.rows):
            yield self[row, 0]

    def __str__(self):
        return "\n".join(str(x) for x in self) + "\n"
    
    def __getitem__(self, key):
        row, col = key
        return self.data[row]
    
    def __setitem__(self, key, value):
        row, col = key
        self.data[row] = value

# self_inverse = Matrix(4, 4, [[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]])
# print(self_inverse)
# print((self_inverse * 0.5) * (self_inverse * 0.5))

# I = Matrix(3, 3, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# tau = Matrix(3, 3, [[0, 1, 0], [1, 0, 0], [0, 0, 1]])
# tau_prime = Matrix(3, 3, [[1, 0, 0], [0, 0, 1], [0, 1, 0]])
# tau_double_prime = Matrix(3, 3, [[0, 0, 1], [0, 1, 0], [1, 0, 0]])
# sigma = Matrix(3, 3, [[0, 0, 1], [1, 0, 0], [0, 1, 0]])
# sigma_prime = Matrix(3, 3, [[0, 1, 0], [0, 0, 1], [1, 0, 0]])

# bin_list = Vector(9, [[1, 0, 1, 1, 0, 1, 0, 0, 1]])
# dec = bin_list.transpose() * Matrix.binary_matrix(bin_list.rows) * bin_list
# print(dec)

# print(I)
# print(I.det())
# print()
# print(sigma)
# print(sigma.det())
# print()
# print(sigma_prime)
# print(sigma_prime.det())
# print()
# print(tau)
# print(tau.det())
# print()
# print(tau_prime)
# print(tau_prime.det())
# print()
# print(tau_double_prime)
# print(tau_double_prime.det())

# print(I.eigenvalues())

base = Matrix(3, 3, [[2, 0, 0], [0, 3, 0], [0, 0, 5]])

#print(base ** 1)


#print(I.inverse())