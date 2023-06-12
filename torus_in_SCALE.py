#!/bin/env python3
#
# Ondrej Chvala <ondrejch@gmail.com>
# MIT license

import math


def SCALE_approximate_torus(id_cyl0, id_boundary, mixture, major_radius, minor_radius, num_cylinders):
    """ Generates SCALE geometry to approximate a torus with a sequence of cylinders.
    id_cyl0         -  Starting SCALE shape ID
    id_boundary     -  Boundary ID
    mixture         -  Material mixture for the cylinder
    major_radius    -  Major radius of the torus
    minor_radius    -  Minor radius of the torus
    num_cylinders   -  How may cylinders to approximate the torus """

    deck = []
    cyl_ids = []

    # side of the outer polygon
    cylinder_height = 2.0 * (major_radius + minor_radius) * math.sin(math.pi / num_cylinders)

    for i in range(num_cylinders):
        angle = i * (2.0 * math.pi / num_cylinders)
        left = -cylinder_height / 2.0
        right = cylinder_height / 2.0
        origin_x = major_radius * math.cos(angle)
        origin_y = major_radius * math.sin(angle)
        origin_z = 0.0
        angle_deg = math.degrees(angle) - 90.0

        shape_id = id_cyl0 + i + 1
        cylinder = f"xcylinder {shape_id} {minor_radius} {right} {left} origin x={origin_x} y={origin_y} z={origin_z} rotate a1={angle_deg}"
        deck.append(cylinder)
        cyl_ids.append(shape_id)

    # bounding box
    cuboid = f"cuboid {id_boundary} 4p{major_radius + 2.0 * minor_radius} 2p{3.0 * minor_radius}"
    deck.append(cuboid)

    # mixtures
    shifted_cyl_ids = [cyl_ids[-1]] + cyl_ids[:-1]
    for i in range(num_cylinders):
        deck.append(f"media {mixture} 1  {cyl_ids[i]} -{shifted_cyl_ids[i]}")

    neg_cyl_ids = " ".join(["-" + str(item) for item in cyl_ids])
    deck.append(f"media 0 1 {id_boundary} {neg_cyl_ids}")
    deck.append(f"boundary {id_boundary}")

    return deck


# Example usage
id_cyl0 = 500           # Starting SCALE shape ID
id_boundary = 9999      # Boundary ID
mixture = 1             # Material mixture for the cylinder
major_radius = 20       # Major radius of the torus
minor_radius = 2        # Minor radius of the torus
num_cylinders = 32      # How may cylinders to approximate the torus

SCALE_torus = SCALE_approximate_torus(id_cyl0, id_boundary, mixture, major_radius, minor_radius, num_cylinders)

header='''=csas6 parm=(   )
torus approximated with cylinders
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
for torus_line in SCALE_torus:
    print(torus_line)
print(footer)
