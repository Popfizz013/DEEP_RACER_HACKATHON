def reward_function(params):
    """
    Reward function for AWS DeepRacer to guide the car toward optimal behavior on the track.

    The function assigns rewards based on the car's position relative to the center line, 
    its heading (to determine if it's on a straightaway or curve), and its steering angle. 
    The goal is to promote smooth driving, maintain track adherence, and minimize unnecessary 
    corrections, ensuring efficient lap completion.

    Args:
        params (dict): A dictionary of parameters provided by the AWS DeepRacer environment. Includes:
            - track_width (float): The width of the track.
            - distance_from_center (float): The distance of the car from the center line of the track.
            - is_left_of_center (bool): True if the car is on the left side of the center line, False otherwise.
            - all_wheels_on_track (bool): True if all wheels of the car are on the track, False otherwise.
            - steering_angle (float): The steering angle of the car in degrees.
            - heading (float): The current heading of the car in degrees.

    Returns:
        float: A reward value indicating how favorable the car's current state is for the given conditions.
    """
    # Retrieve track and positional parameters
    track_width: float = params['track_width']  # Total width of the racing track
    distance_from_center: float = params['distance_from_center']  # Deviation from the center line
    left: bool = params["is_left_of_center"]  # Boolean indicating if car is on the left of the center
    on_track: bool = params["all_wheels_on_track"]  # True if all wheels remain on track surface

    # Retrieve steering and heading parameters
    abs_steering: float = abs(params['steering_angle'])  # Absolute steering angle for penalty calculations
    cur_heading: float = params["heading"]  # Vehicle's current heading in degrees, used to detect straight paths

    # Detect if the car is on a straightaway
    # Straight paths are defined as those where the heading is close to zero (-10° to 10°)
    on_straight: bool = False
    if -10 <= cur_heading <= 10:
        on_straight = True

    # Divide the track into three zones based on proximity to the center line
    quad_1 = 0.25 * track_width  # Zone closest to the center line
    quad_2 = 0.50 * track_width  # Intermediate zone
    quad_3 = 0.75 * track_width  # Farthest zone still considered "on track"

    # Initialize reward to a neutral value
    reward = 0

    # Reward logic for straightaways
    if on_straight:
        # Encourage the car to stay in favorable zones for smoother motion
        if left:
            if quad_1 <= distance_from_center <= quad_2:
                reward = 0.8  # Optimal positioning on the left during straight paths
            elif distance_from_center <= quad_3 and on_track:
                reward = 0.4  # Lesser reward for staying within track bounds but not optimal
        else:
            if quad_1 <= distance_from_center <= quad_2:
                reward = 1  # Optimal positioning on the right
            elif distance_from_center <= quad_3 and on_track:
                reward = 0.5  # Moderate reward for non-ideal but valid positioning
    else:
        # Reward logic for curves (non-straight sections)
        if left:
            if quad_1 <= distance_from_center <= quad_2:
                reward = 1  # Optimal reward for keeping close to the center on left curves
            elif distance_from_center <= quad_3 and on_track:
                reward = 0.5  # Lesser reward for staying within bounds but off-center
        else:
            if distance_from_center <= quad_1:
                reward = 0.5  # Moderate reward for staying close to the center
            elif distance_from_center <= quad_2:
                reward = 0.1  # Minimal reward for being farther away
            else:
                reward = 1e-3  # Significant penalty for straying too far from the center

    # Penalize excessive steering
    # Excessive steering indicates abrupt or unnecessary corrections, which destabilize the car
    ABS_STEERING_THRESHOLD = 15  # Threshold in degrees beyond which steering is penalized
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8  # Reduce reward by 20% for high steering angles

    return float(reward)