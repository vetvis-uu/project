# Read the CSV file and convert the latitude and longitude into x,y-coordinates into Kilometers.
# Anders Hast 5/6-2013 (modified by Fredrik Nysjo 2020)

import vtk

import string
import math
import time


#Read Points
def readPoints(file, depth_scaling=0.01):
    # Create an array of Points
    points = vtk.vtkPoints()
    # Create arrays of Scalars
    scalars = vtk.vtkFloatArray()
    tid     = vtk.vtkFloatArray()
    depth   = vtk.vtkFloatArray()

    # Initialize
    LatMax=0
    LatMin=360
    LonMax=0
    LonMin=360
    tMin=99999999999999

    # Open the file
    file = open(file)
    
    # Read one line
    line = file.readline()

    # Loop through lines
    tMin = 1.0e15
    while line:
        # Split the line into data
        data = line.split('|')
        # Skip the commented lines
        if data and data[0][0] != '#':
            # Convert data into float
            print(data[0], data[1], data[2], data[3], data[4].split('--')[0], data[10])

            date, x, y, z, r = data[1], float(data[2]), float(data[3]),  float(data[4]), float(data[10])
            z_scaled = z * depth_scaling
            row=date.split('T')
            adate=row[0].split('-')
            atime=row[1].split(':')
            temp=atime[2].split('.')
            atime[2]=temp[0]

            if atime[2]=='':
                atime[2]='00'
            t= time.mktime((int(adate[0]),int(adate[1]),int(adate[2]),int(atime[0]),int(atime[1]),int(atime[2]),0,0,0))
            
            if x > LatMax:
                LatMax=x
            if x< LatMin:
                LatMin=x
            if y > LonMax:
                LonMax=y
            if y< LonMin:
                LonMin=y
            if t< tMin:
                 tMin=t
            
            # Insert floats into the point array
            points.InsertNextPoint(x, y, z_scaled)
            scalars.InsertNextValue(r)
            t -= 1467247524.0  #FIXME
            tid.InsertNextValue(t)
            depth.InsertNextValue(z_scaled)

        # read next line
        line = file.readline()
        
    print(LatMin, LatMax, LonMin, LonMax)

    return points, scalars, tid, depth
