#!/bin/env python3
#
# Ondrej Chvala <ondrejch@gmail.com>
# MIT license

import math


def SCALE_approximate_toroidal_pipe(id_start, id_boundary, mixture_inside, mixture_wall, major_radius, minor_radius_inside, minor_radius_outside, num_cylinders, X, Y, Z):
    """ Generates SCALE geometry to approximate a torus with a sequence of cylinders.
    id_start             -  Starting SCALE shape ID
    id_boundary          -  Boundary ID
    mixture_inside       -  Material mixture for inside the pipe
    mixture_wall         -  Material mixture for the pipe walls
    major_radius         -  Major radius of the torus
    minor_radius_inside  -  Minor radius of the torus, inside pipe
    minor_radius_outside -  Minor radius of the torus, outide pipe
    num_cylinders        -  How may cylinders to approximate the torus
    X, Y, Z              -  Move global origen to [X,Y,Z,]   """


    deck = []
    cyl_ids_inside = []
    cyl_ids_outside = []

    cylinder_height = 2.0 * (major_radius + minor_radius_inside) * math.sin(math.pi / num_cylinders)
    # Inside
    for i in range(num_cylinders):
        angle = i * (2.0 * math.pi / num_cylinders)
        left = -cylinder_height / 2.0
        right = cylinder_height / 2.0
        origin_x = major_radius * math.cos(angle) + X
        origin_y = major_radius * math.sin(angle) + Y
        origin_z = Z
        angle_deg = math.degrees(angle) - 90.0

        shape_id = id_start + i + 1
        cylinder = f"xcylinder {shape_id} {minor_radius_inside} {right} {left} origin x={origin_x} y={origin_y} z={origin_z} rotate a1={angle_deg}"
        deck.append(cylinder)
        cyl_ids_inside.append(shape_id)

    # Outide
    for i in range(num_cylinders):
        angle = i * (2.0 * math.pi / num_cylinders)
        left = -cylinder_height / 2.0
        right = cylinder_height / 2.0
        origin_x = major_radius * math.cos(angle) + X
        origin_y = major_radius * math.sin(angle) + Y
        origin_z = Z
        angle_deg = math.degrees(angle) - 90.0

        shape_id = id_start + num_cylinders + i + 1
        cylinder = f"xcylinder {shape_id} {minor_radius_outside} {right} {left} origin x={origin_x} y={origin_y} z={origin_z} rotate a1={angle_deg}"
        deck.append(cylinder)
        cyl_ids_outside.append(shape_id)

    # bounding box
    cuboid = f"cuboid {id_boundary} 4p{major_radius + 2.0 * minor_radius_outside} 2p{3.0 * minor_radius_outside}"
    deck.append(cuboid)

    # mixtures inside
    shifted_cyl_ids_inside = [cyl_ids_inside[-1]] + cyl_ids_inside[:-1]
    shifted_cyl_ids_outside = [cyl_ids_outside[-1]] + cyl_ids_outside[:-1]

    for i in range(num_cylinders):
        deck.append(f"media {mixture_inside} 1  {cyl_ids_inside[i]} -{shifted_cyl_ids_inside[i]} -{shifted_cyl_ids_outside[i]} ")

    # mixtures outside
    for i in range(num_cylinders):
        deck.append(f"media {mixture_wall} 1  {cyl_ids_outside[i]} -{shifted_cyl_ids_outside[i]} -{cyl_ids_inside[i]} ")
#        deck.append(f"media {mixture_wall} 1  {cyl_ids_outside[i]} -{shifted_cyl_ids_outside[i]} -{cyl_ids_inside[i]} -{shifted_cyl_ids_inside[i]}")

    neg_cyl_ids_inside = " ".join(["-" + str(item) for item in cyl_ids_inside])
    neg_cyl_ids_outside = " ".join(["-" + str(item) for item in cyl_ids_outside])
    deck.append(f"media 0 1  {id_boundary} {neg_cyl_ids_inside} {neg_cyl_ids_outside}")
    deck.append(f"boundary {id_boundary}")

    return deck

#
# Example usage
#
id_start = 500                  # Starting SCALE shape ID
id_boundary = 9999              # Boundary ID
mixture_inside= 1               # Material mixture inside the pipe
mixture_wall= 2                 # Material mixture for the pioe wall
major_radius = 20               # Major radius of the torus
minor_radius_inside  = 2        # Minor radius of the torus, inside pipe
minor_radius_outside = 3        # Minor radius of the torus, outide pipe
num_cylinders = 32              # How may cylinders to approximate the torus
X = 0                           # Move global origen to [X,Y,Z]
Y = 0                           # Move global origen to [X,Y,Z]
Z = 5                           # Move global origen to [X,Y,Z]

SCALE_tor_pipe = SCALE_approximate_toroidal_pipe(id_start, id_boundary, mixture_inside, mixture_wall, major_radius, minor_radius_inside, minor_radius_outside, num_cylinders, X, Y, Z)


header='''=csas6 parm=(   )
toroidial pipe
ce_v7.1_endf

read comp
 water 1    end
 ss304 2    end
end comp

read geometry
global unit 1
'''

footer='''end geometry
end data
end
'''

# Print the SCALE deck piece
print(header)
for pipe_line in SCALE_tor_pipe:
    print(pipe_line)
print(footer)
