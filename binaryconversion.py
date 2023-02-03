from Matrix import *

def bin2dec(bin_vector):
    A = Matrix.binary_matrix(bin_vector.size)
    dec = bin_vector.transpose() * A * bin_vector
    return dec

bin_vector = Vector(8, [1, 0, 0, 1, 1, 1, 1, 0])
bin2dec