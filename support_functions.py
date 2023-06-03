from numpy import sin, cos, pi


# Used by Cartpole and Acrobot
def get_average(time_steps):
    # Total number of elements
    num_elements = len(time_steps) - 1
    # Calculate average time steps
    if num_elements <= 100:
        # Divide current cumulative time steps if < 100
        return time_steps[-1] / num_elements
    else:
        # Divide last 100 cumulative time steps if >= 100
        return (time_steps[-1] - time_steps[-101]) / 100


# Used by Cartpole
def future_position(obv):
    _, _, angle, velocity = obv
    threshold = pi / 15
    new_angle = angle + 0.02 * velocity
    terminated = new_angle < -threshold or new_angle > threshold
    return new_angle, terminated


# Used by Cartpole
def angle_reward(obv):
    angle, _ = future_position(obv)
    return max(pi / 15 - abs(angle), 0)


# Used by Acrobot
def _dsdt(s_augmented):
    m1 = 1.0  #: [kg] mass of link 1
    m2 = 1.0  #: [kg] mass of link 2
    l1 = 1.0  # [m]
    lc1 = 0.5  #: [m] position of the center of mass of link 1
    lc2 = 0.5  #: [m] position of the center of mass of link 2
    I1 = 1.0  #: moments of inertia for both links
    I2 = 1.0  #: moments of inertia for both links
    g = 9.8

    a = s_augmented[-1]
    s = s_augmented[:-1]

    theta1 = s[0]
    theta2 = s[1]
    dtheta1 = s[2]
    dtheta2 = s[3]

    d1 = (m1 * lc1 ** 2 + m2 * (l1 ** 2 + lc2 ** 2 + 2 * l1 * lc2 * cos(theta2)) + I1 + I2)
    d2 = m2 * (lc2 ** 2 + l1 * lc2 * cos(theta2)) + I2

    phi2 = m2 * lc2 * g * cos(theta1 + theta2 - pi / 2.0)
    phi1 = (-m2 * l1 * lc2 * dtheta2 ** 2 * sin(theta2) - 2 * m2 * l1 * lc2 * dtheta2 * dtheta1 * sin(theta2)
            + (m1 * lc1 + m2 * l1) * g * cos(theta1 - pi / 2) + phi2)

    # the following line is consistent with the java implementation and the book
    ddtheta2 = (a + d2 / d1 * phi1 - m2 * l1 * lc2 * dtheta1 ** 2 * sin(theta2) - phi2) / (
            m2 * lc2 ** 2 + I2 - d2 ** 2 / d1)
    ddtheta1 = -(d2 * ddtheta2 + phi1) / d1

    return dtheta1, dtheta2, ddtheta1, ddtheta2, 0.0
