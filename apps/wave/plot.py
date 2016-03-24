""" Reads in the 1D wave equation solution data, written by the OPS dat writer,
and plots the scalar field 'phi'. """

import argparse
import numpy
from math import pi, exp, cos, sin
import matplotlib.pyplot as plt
import h5py

def plot(path):
    # Number of grid points
    nx = 1000
    
     # Number of halo nodes at each end
    halo = 2

    # Read in the simulation output
    f = h5py.File(path + "/state.h5", 'r')
    group = f["wave_block"]
    
    phi = group["phi"].value
    
    # Ignore the 2 halo nodes at either end of the domain
    phi = phi[halo:nx+halo]
    print phi
    # Grid spacing
    dx = 1.0/(nx);
    
    # Coordinate array
    x = numpy.zeros(nx)
    phi_analytical = numpy.zeros(nx)
    phi_error = numpy.zeros(nx)

    # Compute the error
    for i in range(0, nx):
        x[i] = i*dx
        # Analytical solution
        phi_analytical[i] = abs(sin(pi*(x[i]+0.5))) # Phi should be a sin wave shifted to the right by x = 0.5 (since the wave speed is 0.5 m/s and we've simulated until T = 1.0 s).
        phi_error[i] = abs(phi_analytical[i] - phi[i])

    plt.plot(x, phi_error, label=r"Absolute error in $\phi$")
    plt.xlabel(r"$x$ (m)")
    plt.ylabel(r"$\phi$")
    plt.legend()
    plt.savefig("phi_error.pdf")
    plt.show()


if(__name__ == "__main__"):
    # Parse the command line arguments provided by the user
    parser = argparse.ArgumentParser(prog="plot")
    parser.add_argument("path", help="The path to the directory containing the output files.", action="store", type=str)
    args = parser.parse_args()
    
    plot(args.path)
