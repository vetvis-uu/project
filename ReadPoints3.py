#To use this you need to install pandas
#This sccript is more roust to new data and works best with python 3 +

import pandas as pd
import numpy as np
import vtk
from vtk.util import numpy_support

def readPoints(file, depth_scaling=0.01, time_shift=-1467247524):

    df=pd.read_csv("data_365days.txt",sep="|")
    df["Magnitude"].isna().values.any()

    df[['Latitude', 'Longitude']]=df[['Latitude', 'Longitude']].clip(lower=0,upper=360)
    df['NewDepth']=df['Depth/Km']*depth_scaling
    df["NewTime"]= pd.to_datetime(df['Time']).values.astype(np.int64) // 10 ** 6

    points=df[['Latitude', 'Longitude', 'NewDepth']].to_numpy()
    times=df["NewTime"].to_numpy()+t_shift
    scalars=df["Magnitude"].to_numpy()
    depth=df["NewDepth"].to_numpy()

    p = vtk.vtkPoints()
    for i in range(points.shape[0]):
        p.InsertNextPoint(points[i,:])
    s = numpy_support.numpy_to_vtk(scalars)
    t = numpy_support.numpy_to_vtk(times)
    d = numpy_support.numpy_to_vtk(depth)

    return p,s,t,d
