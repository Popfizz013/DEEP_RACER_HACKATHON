# Working reward function for mode stinkMobile

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''

    # Initialize reward as the "penalty"
    reward = 1e-3 

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    left = params["is_left_of_center"]
    on_track= params["all_wheels_on_track"]

    # Calculate 3 markers that are at varying distances away from the center line
    quad_1 = 0.25 * track_width
    quad_2 = 0.50 * track_width
    quad_3 = 0.75 * track_width
    
    if left:
        if (distance_from_center <= quad_2 and distance_from_center>= quad_1):
            reward=1
        elif (distance_from_center <= quad_3 and on_track):
            reward=0.5 
    else:
        # Give higher reward if the car is closer to center line and vice versa
        if distance_from_center <= quad_1:
            reward = 0.5
        elif distance_from_center <= quad_2:
            reward = 0.1

    return float(reward)