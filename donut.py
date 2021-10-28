import math

# To draw a circle on 2D, we plot the points for each change in theta {0..2pi} according to the equation (R1 cos theta, R1 sin theta, 0) to get (x, y, z)
# Change in theta value is represented by theta_spacing
theta_spacing = 0.07
# To rotate a circle about y-axis, we multiple it by a rotation matrix along phi
# Change in phi value is represented by phi_spacing
phi_spacing = 0.02

# Screen width and height
screen_width = 40
screen_height = 40

# Radius of torus from center point to inner circle
R1 = 1
# Radius of torus from center point to outer circle
R2 = 2
# Distance of the donut from the viewer
K2 = 5
# Refers to z' which is distance of eye to screen
# Controls the scale, which depends on pixel resolution
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))

# Rate of change in angle of rotation in one axis
A_delta = 0.08
# Rate of change in angle of rotation in one axis, in opposite direction of A
B_delta = 0.03

# For how many frames do you want this to loop
loop_time = 2000


def render_frame(A, B):
    # precompute sines and cosines of A and B
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    char_output = []  # characters for each frame
    zbuffer = []  # z coordinates of every pixel

    # initialise char_output and zbuffer with spaces and zeros
    for i in range(screen_height + 1):
        char_output.append([" "] * screen_width)
        zbuffer.append([0] * screen_width)

    # theta goes from 0 to 2pi, this is to draw a circle on 2D
    theta = 0
    while theta < 2 * math.pi:
        # Increment theta by theta_spacing to get the next point
        # Do this until 2 * math.pi to get a full circle
        theta += theta_spacing

        # precompute sines and cosines of theta
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # phi goes from 0 to 2pi, this is to rotate a circle about y-axis
        phi = 0
        while phi < 2 * math.pi:
            phi += phi_spacing

            # Precompute sines and cosines of phi
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            # x, y coordinate of the circle before revolving
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D coordinate after rotations, directly from equation above
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z  # depth of the pixel

            # x and y projection. y is negated because y goes up in 3D space but down on 2D displays
            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            # Calculate luminance of the pixels
            # This is done by matrix multiplying the surface normal with light source from the back of the object (0, 1, -1)
            L = (
                cosphi * costheta * sinB
                - cosA * costheta * sinphi
                - sinA * sintheta
                + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            )

            # L ranges from -sqrt(2) to +sqrt(2). If it is less than 0, this means surface is pointing away from us, so we don't plot it
            if L > 0:
                # Check against z-buffer. Larger 1/z (ooz) means pixel is closer to the viewer than what is already plotted
                if ooz > zbuffer[xp][yp]:
                    zbuffer[xp][yp] = ooz
                    # brings L to {0..11.3} since 8*sqrt(2) = 11.3
                    luminance_index = L * 8

                    # Lookup the character corresponding to the luminance and store
                    char_output[xp][yp] = ".,-~:;=!*#$@"[int(luminance_index)]
    # clear screen
    print("\x1b[H")
    for i in range(screen_height):
        for j in range(screen_width):
            print(char_output[i][j], end="")
        print()


def main():
    print("\x1b[2J")
    print(" ##################################################################")
    print(" #  Spinning donut created by Derek Chia (https://derekchia.com)  #")
    print(" #  See annotated code at https://github.com/derekchia/donut-math #")
    print(" ##################################################################")
    A = 1.0
    B = 1.0
    # loop through each frame
    for i in range(loop_time):
        # with each frame, increment A and B by their respective delta values
        render_frame(A, B)
        A += A_delta
        B += B_delta


if __name__ == "__main__":
    main()
