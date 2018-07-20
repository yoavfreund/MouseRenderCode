#!/usr/bin/env python

"""
This example shows how to create an unstructured grid.
"""

import vtk
import numpy as np
import pickle as pkl

colors_list = pkl.load(open('permuted_colors.pkl','rb'))

def main():
    colors = vtk.vtkNamedColors()

    Data=np.load('tessaltions_compressed.npz')

    indices=Data['index']
    
    renderer = vtk.vtkRenderer()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    for index in indices:
        x=Data['points_'+str(index)]
        triangles = Data['triangles_'+str(index)]
        print(index,x.shape, triangles.shape,'\r',end='')

        points = vtk.vtkPoints()
        for i in range(0, x.shape[0]):
            points.InsertPoint(i, x[i,:])

        ugrid = vtk.vtkUnstructuredGrid()
        ugrid.Allocate(triangles.shape[0])
        for i in range(triangles.shape[0]):
            ugrid.InsertNextCell(vtk.VTK_TRIANGLE, 3, triangles[i,:])

        ugrid.SetPoints(points)

        ugridMapper = vtk.vtkDataSetMapper()
        ugridMapper.SetInputData(ugrid)

        ugridActor = vtk.vtkActor()
        ugridActor.SetMapper(ugridMapper)
        ugridActor.GetProperty().SetColor(colors.GetColor3d(colors_list[index]))
        ugridActor.GetProperty().EdgeVisibilityOff()
        ugridActor.GetProperty().SetOpacity(0.4)

        renderer.AddActor(ugridActor)

    renderer.SetBackground(colors.GetColor3d('Beige'))

    renderer.ResetCamera()
    renderer.GetActiveCamera().Elevation(60.0)
    renderer.GetActiveCamera().Azimuth(30.0)
    renderer.GetActiveCamera().Dolly(1.2)

    renWin.SetSize(640, 480)

    # Interact with the data.
    renWin.Render()

    iren.Start()


if __name__ == "__main__":
    main()
