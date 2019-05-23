import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if(self.h ==1):
            return self[0][0]
        else:
            return (self[0][0]*self[1][1] - self[0][1]*self[1][0])

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        trace_val =0
        for i in range(self.h):
            for j in range(self.w):
                if(i==j):
                    trace_val += self[i][j]
        return trace_val

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        det = self.determinant()
        inv_mat = zeroes(self.h,self.w)
        if (self.h ==1):
            inv_mat[0][0]= (1/det)         
        else:            
            for i in range(self.h):                
                for j in range(self.w):
                    if(i==0 and j==0):
                        inv_mat[0][0] = (self[1][1]) / det 
                    elif(i==1 and j==1):
                        inv_mat[1][1]= (self[0][0]) / det 
                    else:
                        inv_mat[i][j] = -(self[i][j]) / det 
        return inv_mat

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        t_self = zeroes(self.w,self.h)   
        for i in range(self.w):            
            for j in range(self.h):
                if(i==j):
                    t_self[i][j]=self[i][j]
                else:
                    t_self[i][j]=self[j][i]
        return Matrix(t_self)

    def is_square(self):
        return self.h == self.w    
    
    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")
        new_mat = []
        for i in range(self.h):
            new_mat.append([])
            for j in range(self.w):
                new_mat[i].append(self[i][j] +other[i][j])
        return Matrix(new_mat)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        neg_mat = []
        for i in range(self.h):
            neg_mat.append([])
            for j in range(self.w):
                neg_mat[i].append(-(self[i][j]))
        return Matrix(neg_mat)
   

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        new_mat = []
        for i in range(self.h):
            new_mat.append([])
            for j in range(self.w):
                new_mat[i].append(self[i][j] - other[i][j])
        return Matrix(new_mat)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        m_rows = self.h
        p_columns = other.w
        p_rows = other.h
        # empty list that will hold the product of AxB
        result = zeroes(m_rows,p_columns)
        
        for i in range(m_rows):
            for j in range(p_columns):
                for k in range(p_rows):
                    result[i][j] += self[i][k] * other[k][j]
        return result


    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        rmul_mat = zeroes(self.h, self.w)
        if isinstance(other, numbers.Number):            
            for i in range(self.h):                
                for j in range(self.w):
                    rmul_mat[i][j] = self[i][j]*other
        return rmul_mat

    