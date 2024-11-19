# Working reward function for mode stinkMobile

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    # Read input parameters
    track_width: float = params['track_width']
    distance_from_center: float = params['distance_from_center']
    left: bool = params["is_left_of_center"]
    on_track: bool= params["all_wheels_on_track"]
    abs_steering: float = abs(params['steering_angle']) # Only need the absolute steering angle

    # Reports x-coordinate 
    cur_heading: float = params["heading"]

    # Flag to indicate if vehicle is on straight away
    on_straight: bool = False

    # Sets flag if vehicle is on straight away
    if ((-10 <= cur_heading) and (cur_heading <= 10)):
        on_straight = True

    # Calculate 3 markers that are at varying distances away from the center line
    quad_1 = 0.25 * track_width
    quad_2 = 0.50 * track_width
    quad_3 = 0.75 * track_width
    
    # Initialize reward
    reward=0
    # Set reward zones to favour wide turns after straight away or tight corners in sequence
    if on_straight:
        if left:
            if (distance_from_center <= quad_2 and distance_from_center>= quad_1):
                reward = 0.8
            elif (distance_from_center <= quad_3 and on_track):
                reward = 0.4 
        else:
            if (distance_from_center <= quad_2 and distance_from_center>= quad_1):
                reward = 1
            elif (distance_from_center <= quad_3 and on_track):
                reward = 0.5 
    elif left:
        if (distance_from_center <= quad_2 and distance_from_center>= quad_1):
            reward = 1
        elif (distance_from_center <= quad_3 and on_track):
            reward = 0.5 
    else:
        # Give higher reward if the car is closer to center line and vice versa
        if distance_from_center <= quad_1:
            reward = 0.5
        elif distance_from_center <= quad_2:
            reward = 0.1
        else:
            reward = 1e-3


    ABS_STEERING_THRESHOLD = 15
    
    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)