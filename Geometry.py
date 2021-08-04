'''This script contains class definitions related to geometry that are used
    by the interactive Triangle_Viewer script..
    
    Name: Nicholas Wood, PhD
    Institution: USNA
    Email: nwood@usna.edu
'''

import numpy as np
import math


class LineSegment:

    '''Defines a line segment. Each instance contains two vectors A and B
        which contain the coordinates of the terminal points of the line.
        It is assumed A and B are NumPy arrays of size 1x2. Additionally there will
        be a method that returns the length of the line segment, and a method
        which returns the midpoint of the line segment.'''

    def __init__(self, A, B, name = None):
        '''A and B are numpy arrays defining the terminal points of the line segment.
            name is the kind of line segment it is (if any), i.e. Leg, Median, etc.'''
        
        self.A = A
        self.B = B
        self._name = name

        #Calculate slope and intercept of this line
        if A[0] != B[0]:
            self._slope = (B[1] - A[1])/(B[0] - A[0])
        else:
            #Vertical line with infinite slope
            self._slope = float('inf')
        

        if self._slope != float('inf'):
            self._intercept = (A[1] - self._slope*A[0])
        else:
            #Vertical line has no y intercept
            self._intercept = float('nan')

    def __str__(self):

        return self._name


    def Length(self):
        '''Calculate and return the length of the line segment.'''

        return math.sqrt(np.dot(self.A - self.B, self.A - self.B))


    def Midpoint(self):
        '''Calculate and return the midpoint of the line segment.'''

        return (self.A + self.B)/2


    def Intersection(self, lineseg):
        '''Determine the point at which this line and lineseg intersect
            (if they were extended as lines).'''

        m1, b1 = self._slope, self._intercept
        m2, b2 = lineseg._slope, lineseg._intercept

        if m2 == m1:
            raise Exception('Parallel lines do not have a unique point at which they intercept!')

        else:

            if m1 == float('inf'):
                x = self.A[0]
                y = m2*x + b2
                
            elif m2 == float('inf'):
                x = lineseg.A[0]
                y = m1*x + b1

            else:
                
                x = (b2 - b1)/(m1 - m2)
                y = m1*x + b1

            return x, y

    def Generate_LineSegment(self):

        return [self.A[0], self.B[0]], [self.A[1], self.B[1]]


class Circle:

    '''Defines a circle. Circles are initialized with center (1x2 numpy array indicating
        the x and y coordingates of the center) and a non-negative radius r.'''

    def __init__(self, center, r):

        self.center = center
        self.r = r


    def Generate_Circle(self):

        center = self.center
        r = self.r

        Theta = np.linspace(0, 2*math.pi, num = 360)

        X = [r*math.cos(theta) + center[0] for theta in Theta]
        Y = [r*math.sin(theta) + center[1] for theta in Theta]

        return X, Y


class Triangle:

    '''Defines a Triangle. Triangles are initialized by three vertices A, B, and C
        which are assumed to be numpy arrays of size 1x2. There will also be many
        methods for this class.'''

    def __init__(self, A, B, C):
        '''A, B, and C are numpy arrays defining the three vertices of the triangle.'''

        #Vertices of the Triangle
        self.Vertices = [A, B, C]

        #Legs of the Triangle
        self.Legs = self.Get_Legs()

        #Sides of the Triangle
        self.Sides = self.Get_Sides()

        #Anglesof the Triangle (in radians)
        self.Angles = self.Get_Angles()

    def Get_Legs(self):
        '''Create the legs of the triangle.'''
        A, B, C = self.Vertices

        return [LineSegment(B, C, 'Leg'), LineSegment(C, A, 'Leg'), LineSegment(A, B, 'Leg')]

    def Get_Sides(self):
        '''Get the sides of the triangle'''

        return [leg.Length() for leg in self.Legs]

    def Get_Angles(self):
        '''Get the angles of the triangle'''

        a, b, c = self.Sides
        return [math.acos((b**2 + c**2 - a**2)/(2*b*c)), math.acos((c**2 + a**2 - b**2)/(2*c*a)), math.acos((a**2 + b**2 - c**2)/(2*a*b))]


    def Generate_Triangle(self):
        '''Return the x and y lists to plot the triangle'''

        X = [v[0] for v in self.Vertices + [self.Vertices[0]]]
        Y = [v[1] for v in self.Vertices + [self.Vertices[0]]]

        return X, Y

    def Generate_Medians(self):
        '''Return a list of lists which are the x and y coordinates for the median lines.'''

        X = []
        Y = []
        for vertex, leg in zip(self.Vertices, self.Legs):
            median = self.Get_Median(vertex, leg)

            X.append([median.A[0], median.B[0]])
            Y.append([median.A[1], median.B[1]])

        return X, Y

    def Generate_PerpendicularBisectors(self):
        '''Return a list of lists which are the x and y coordinates for the perpendicula bisectors.'''

        X = []
        Y = []
        for vertex, leg in zip(self.Vertices, self.Legs):
            median = self.Get_PerpendicularBisector(vertex, leg)

            X.append([median.A[0], median.B[0]])
            Y.append([median.A[1], median.B[1]])

        return X, Y

    def Generate_AngleBisectors(self):
        '''Return a list of lists which are the x and y coordinates for the angle bisectors.'''

        X = []
        Y = []
        for vertex, leg in zip(self.Vertices, self.Legs):
            median = self.Get_AngleBisector(vertex, leg)

            X.append([median.A[0], median.B[0]])
            Y.append([median.A[1], median.B[1]])

        return X, Y

    def Generate_Altitudes(self):
        '''Return a list of lists which are the x and y coordinates for the altitudes.'''

        X = []
        Y = []
        for vertex, leg in zip(self.Vertices, self.Legs):
            median = self.Get_Altitude(vertex, leg)

            X.append([median.A[0], median.B[0]])
            Y.append([median.A[1], median.B[1]])

        return X, Y


    def Get_Median(self, vertex, leg):
        '''A Median connects a vertex to the midpoint of the opposite side.
            This method returns a line segment which is that median line.'''

        midpoint = leg.Midpoint()

        return LineSegment(vertex, midpoint, 'Median')

    

    def Get_Altitude(self, vertex, leg):
        '''The Altitude goes through a vertex and is perpendicular to the opposite side.'''

        #First determine the slope of the leg
        slope = leg._slope

        #Next determine the slope of the line which is perpendicular to the leg
        if slope == float('inf'):
            #Horizontal line
            slope = 0

        elif slope == 0:
            #Vertical line
            slope = float('inf')

        else:
            slope = -1/slope


        #Now determine another point on the altitude besides the vertex
        if slope == 0:
            #Horizontal line
            lineseg = LineSegment(vertex, vertex + np.array([1, 0]))

        elif slope == float('inf'):
            #Vertical Line
            lineseg = LineSegment(vertex, vertex + np.array([0, 1]))

        else:
            x1, y1 = vertex
            x = x1 + 1
            y = slope*x + (-slope*x1 + y1)

            lineseg = LineSegment(vertex, np.array([x, y]))

        x, y = lineseg.Intersection(leg)


        return LineSegment(vertex, np.array([x, y]), 'Altitude')


    def Get_PerpendicularBisector(self, vertex, leg):
        '''Perpendicular Bisectors connects the midpoint to the Circumcenter.'''

        mp = leg.Midpoint()
        x, y = self.Generate_Circumcenter()
        cc = np.array([x, y])

        return LineSegment(mp, cc, 'Perpendicular Bisector')


    def Get_AngleBisector(self, vertex, leg):
        '''The angle bisector connects the vertex to the leg, passing through the
            incenter.'''

        x, y = self.Generate_Incenter()
        ic = np.array([x, y])

        #Connect the incenter to the vertex
        lineseg = LineSegment(ic, vertex)

        #Determine where that linesegment intersects with the leg
        x, y = lineseg.Intersection(leg)

        return LineSegment(vertex, np.array([x, y]), 'Angle Bisector')
    

    def Generate_Centroid(self):
        '''Determines the centroid of the triangle and returns a center object.'''

        A, B, C = self.Vertices

        #Centroid is simply the average of the three vertice coordinates
        P = (A + B + C)/3

        return P[0], P[1]


    def Generate_Incenter(self):
        '''Determines the incenter of the triangle and returns a center object.'''

        a, b, c = self.Sides
        A, B, C = self.Vertices

        p = a + b + c

        x = (a*A[0] + b*B[0] + c*C[0])/p
        y = (a*A[1] + b*B[1] + c*C[1])/p

        

        return x, y

    def Generate_Circumcenter(self):
        '''Determines the circumcenter of the triangle and returns a center object.'''

        

        X = [v[0] for v in self.Vertices]
        Y = [v[1] for v in self.Vertices]

        alpha = 2*(-X[0] + X[1])
        beta = 2*(-Y[0] + Y[1])
        gamma = 2*(-X[1] + X[2])
        delta = 2*(-Y[1] + Y[2])

        epsilon = X[1]**2 + Y[1]**2 - X[0]**2 - Y[0]**2
        xi = X[2]**2 + Y[2]**2 - X[1]**2 - Y[1]**2

        mat = np.matrix([[alpha, beta], [gamma, delta]])
        inv_mat = np.linalg.inv(mat)

        P = inv_mat*np.matrix([epsilon, xi]).T
        P = np.array([np.matrix.item(P[i]) for i in range(2)])

        return P[0], P[1]


    def Generate_Orthocenter(self):
        '''Determines the orthocenter of the triangle and returns a center object.'''

        A, B, C = self.Vertices
        leg_A, leg_B, leg_C = self.Legs

        #Calculate any two altitudes
        Alt_A = self.Get_Altitude(A, leg_A)
        Alt_B = self.Get_Altitude(B, leg_B)

        #Determine where those two altitudes intersect
        x, y = Alt_A.Intersection(Alt_B)

        return x, y


    def Generate_Inscribed(self):

        a, b, c = self.Sides
        x, y = self.Generate_Incenter()

        s = (a + b + c)/2
        r = ((s-a)*(s-b)*(s-c)/s)**(1/2)

        inscribed = Circle([x, y], r)

        X, Y = inscribed.Generate_Circle()

        return X, Y


    def Generate_Circumscribed(self):

        x, y = self.Generate_Circumcenter()
        x2, y2 = self.Vertices[0][0], self.Vertices[0][1]

        r = ((x - x2)**2 + (y - y2)**2)**(1/2)

        circumscribed = Circle([x, y], r)

        X, Y = circumscribed.Generate_Circle()

        return X, Y



    
        
