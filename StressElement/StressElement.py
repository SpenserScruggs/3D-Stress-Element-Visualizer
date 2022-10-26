import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin

'''
The purpose of this program is to visualize the 3d stress element 
and the transformation that comes with finding the principal 
stresses and their directions. The red cube is the original stress element
with the red arrows being the original normal stresses. the blue cube is the 
transformed stress element that alligns with the principle stresses, while 
the blue arrows are the principle stresses, found by calculating the eigenvectors
of the cauchy stress tensor. links to relavent articles can be found below.
https://en.wikipedia.org/wiki/Cauchy_stress_tensor
https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors
https://en.wikipedia.org/wiki/Rotation_matrix
'''


Quit = False

while not Quit:
    
    print("\n       -- Enter Normal And Shear Stresses -- ")
    print(" (if you want 2D let Sigma Z, Tau xz, and Tau yz = 0)\n")
    
    check = False
    while not check:
        try:
            Fx = float(input("Sigma X: "))
            Fy = float(input("Sigma Y: "))
            Fz = float(input("Sigma Z: "))
            Vxy = float(input("Tau xy: "))
            Vxz = float(input("Tau xz: "))
            Vyz = float(input("Tau yz: "))
            check = True
        except ValueError:
            print("\nPlease enter a number\n")

    # Stress Tensor
    A = [[Fx, Vxy, Vxz], 
         [Vxy, Fy, Vyz], 
         [Vxz, Vyz, Fz]]

    # calculating principal stresses
    eigval, eigvect = np.linalg.eigh(A)
    eigvect = np.round(eigvect, 5)
    eigval = np.round (eigval, 5)

    print("\nEigen Values: ")
    print(eigval, "\n")

    print("Eigenvectors (x, y, z): ")
    print(eigvect[:, 0])
    print(eigvect[:, 1])
    print(eigvect[:, 2])

    # generating points for the cube
    points = np.array([[1.0, 1.0, 1.0], 
                       [1.0, -1.0, 1.0], 
                       [-1.0, -1.0, 1.0], 
                       [-1.0, 1.0, 1.0], 
                       [1.0, 1.0, 1.0], 
                       [1.0, 1.0, -1.0], 
                       [1.0, -1.0, -1.0], 
                       [1.0, -1.0, 1.0],
                       [1.0, -1.0, -1.0],
                       [-1.0, -1.0, -1.0], 
                       [-1.0, -1.0, 1.0],
                       [-1.0, -1.0, -1.0],
                       [-1.0, 1.0, -1.0],
                       [-1.0, 1.0, 1.0],
                       [-1.0, 1.0, -1.0], 
                       [1.0, 1.0, -1.0]])

    original_points = points.copy()

    # rotating points
    for i in range(len(points)):
        points[i] = np.dot(points[i], np.transpose(eigvect))
        

    # assigning P1 P2 and P3
    stress = [0, 0, 0]
    for i in range(len(eigval)):
        if eigval[i] == max(eigval):
            stress[i] = "P1"
        elif eigval[i] == min(eigval):
            stress[i] = "P3"
        else:
            stress[i] = "P2"

    # drawing the graph
    ax = plt.axes(projection="3d")

    ax.plot(original_points[:, 0] * np.sqrt(3), original_points[:, 1] * np.sqrt(3), original_points[:, 2] * np.sqrt(3), color="red", linestyle='dashed')
    ax.plot(points[:, 0], points[:, 1], points[:, 2], color="blue")

    ax.quiver(eigvect[0, 0], eigvect[1, 0], eigvect[2, 0], eigvect[0, 0] * 3, eigvect[1, 0] * 3, eigvect[2, 0] * 3, color="blue")
    ax.quiver(eigvect[0, 1], eigvect[1, 1], eigvect[2, 1], eigvect[0, 1] * 3, eigvect[1, 1] * 3, eigvect[2, 1] * 3, color="blue")
    ax.quiver(eigvect[0, 2], eigvect[1, 2], eigvect[2, 2], eigvect[0, 2] * 3, eigvect[1, 2] * 3, eigvect[2, 2] * 3, color="blue")

    ax.text(eigvect[0, 0] * 4, eigvect[1, 0] * 4, eigvect[2, 0] * 4, stress[0] + ": " + str(eigval[0]))
    ax.text(eigvect[0, 1] * 4, eigvect[1, 1] * 4, eigvect[2, 1] * 4, stress[1] + ": " + str(eigval[1]))
    ax.text(eigvect[0, 2] * 4, eigvect[1, 2] * 4, eigvect[2, 2] * 4, stress[2] + ": " + str(eigval[2]))

    ax.quiver(np.sqrt(3), 0, 0, 3, 0, 0, color="red", linestyle="dashed")
    ax.quiver(0, np.sqrt(3), 0, 0, 3, 0, color="red", linestyle="dashed")
    ax.quiver(0, 0, np.sqrt(3), 0, 0, 3,  color="red", linestyle="dashed")

    ax.text(4.5, 0, 0, r'$\sigma$x: ' + str(Fx))
    ax.text(0, 4.5, 0, r'$\sigma$y: ' + str(Fy))
    ax.text(0, 0, 4.5, r'$\sigma$z: ' + str(Fz))

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_zlim3d(-2.5, 2.5)
    ax.set_xlim3d(-3, 3)
    ax.set_ylim3d(-3, 3)

    ax.text2D(-0.3, 1.1, r'$\sigma$ X: ' + str(Fx), transform=ax.transAxes)
    ax.text2D(-0.3, 1.05, r'$\sigma$ Y: ' + str(Fy), transform=ax.transAxes)
    ax.text2D(-0.3, 1, r'$\sigma$ Z: ' + str(Fz), transform=ax.transAxes)
    ax.text2D(-0.3, 0.95, r'$\tau$ xy: ' + str(Vxy), transform=ax.transAxes)
    ax.text2D(-0.3, 0.9, r'$\tau$ xz: ' + str(Vxz), transform=ax.transAxes)
    ax.text2D(-0.3, 0.85, r'$\tau$ yz: ' + str(Vyz), transform=ax.transAxes)

    ax.text2D(1.1, 1.1, stress[0] + ": " + str(round(eigval[0], 3)), transform=ax.transAxes)
    ax.text2D(1.1, 1.05, stress[1] + ": " + str(round(eigval[1], 3)), transform=ax.transAxes)
    ax.text2D(1.1, 1, stress[2] + ": " + str(round(eigval[2], 3)), transform=ax.transAxes)

    plt.show()

    print('\n      --       Type (quit) to quit       --\n      --     leave blank to continue     --\n\n')
    awns = input()
    if awns == 'quit':
        Quit = True
    else:
        continue

