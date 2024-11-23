

# AWS DeepRacer Hackathon  

The **AWS DeepRacer Hackathon**, organized by the University of Victoria, provided us with an excellent chance to examine **Reinforcement Learning (RL)** and apply it to real-world autonomous racing. Our project, **stinkMobile**, offers creative techniques to achieve efficient and consistent performance on both virtual and actual tracks.
---

## Event Overview  

AWS DeepRacer challengend students to train RL models in the cloud using **AWS DeepRacer virtual simulator** and deploy them on a 1/18th scale AI-powered car. The competition consisted of simulation/virtual training with also physical track testing, ending in a race day where all teams compete.  


## Our Approach  

### Reward Function  

The reward function is the foundation of our RL model, guiding the car during training. Our latest iteration incorporates dynamic adjustments based on track characteristics, such as straightaways and curves, as well as penalties for excessive steering.  

```python
def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    # Read input parameters
    track_width: float = params['track_width']
    distance_from_center: float = params['distance_from_center']
    left: bool = params["is_left_of_center"]
    on_track: bool = params["all_wheels_on_track"]
    abs_steering: float = abs(params['steering_angle'])  # Absolute steering angle
    cur_heading: float = params["heading"]

    # Flag to indicate if vehicle is on a straightaway
    on_straight: bool = False
    if -10 <= cur_heading <= 10:
        on_straight = True

    # Calculate markers at varying distances from the centerline
    quad_1 = 0.25 * track_width
    quad_2 = 0.50 * track_width
    quad_3 = 0.75 * track_width

    # Initialize reward
    reward = 0

    # Adjust rewards based on straightaway or curved sections
    if on_straight:
        if left:
            if quad_1 <= distance_from_center <= quad_2:
                reward = 0.8
            elif distance_from_center <= quad_3 and on_track:
                reward = 0.4
        else:
            if quad_1 <= distance_from_center <= quad_2:
                reward = 1
            elif distance_from_center <= quad_3 and on_track:
                reward = 0.5
    else:
        if left:
            if quad_1 <= distance_from_center <= quad_2:
                reward = 1
            elif distance_from_center <= quad_3 and on_track:
                reward = 0.5
        else:
            if distance_from_center <= quad_1:
                reward = 0.5
            elif distance_from_center <= quad_2:
                reward = 0.1
            else:
                reward = 1e-3

    # Penalize for excessive steering
    ABS_STEERING_THRESHOLD = 15
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
```

#### Key Improvements:

1. **Straightaway Optimization:**  
   - A flag system detects when the car is on a straight section of the track, encouraging smoother driving.  
   - Adjusted rewards for slight deviations from the center to favor stability on straight paths.  

2. **Dynamic Turning Rewards:**  
   - Wider reward zones encourage strategic turns after straightaways.  
   - Higher penalties for straying too far from the center on curves.  

3. **Steering Control:**  
   - A steering penalty prevents oversteering, improving lap consistency.  

---

### Strategies  

#### Simulation Training  

1. **Initial Testing:**  
   - The model was trained using the **AWS DeepRacer virtual simulator**, providing valuable metrics like lap times and track completion rates.  

2. **Iterative Reward Function Refinement:**  
   - Observed challenges, such as sharp turns and steering inefficiencies, informed adjustments to the reward function.  

3. **Hyperparameter Tuning:**  
   - Optimized parameters such as learning rate and exploration vs. exploitation balance to improve adaptability and learning speed.  

   **Simulation Video Testing**
   -<video controls src="Recording 2024-11-18 220446.mp4" title="Title"></video>
   -<video controls src="Recording 2024-11-18 222013.mp4" title="Title"></video>

#### Physical Testing (November 18th)  

- **Real-World Testing:**  
  - We analyzed how environmental factors like track irregularities impacted performance along with
   actual run times. It seemed that even though the **stinkMobile** was consistent around the track through virtual simulation, the beginning of the Real World testing the car would love to go straight because of the reward system implememted and the car taught itself to go straight dominantly on some test laps, the stinkMobile would take some turns well and was excellent at sticking to the left.  

- **Challenges**  
  - The biggest challenge we ran into was with our reward function, where on testing day we observed our AI car model loved to go straight. Due to that fact the AI car would have some difficulties in taking turns due to our reward function code as we wanted to reward our AI car a good amount therefore the car taught it self to go straight more dominantly.
  - Another issue that occured was as we wanted to take advanatge of curves and momentun on the turns for maximizing the time on the lap
  -An additional challenge we ran into was deciding which model to use, as we had intially tested our model 3 at the in person testing and it did not do as well as expected resulting in a significantly lower time in comparison to a model 2 where we trained which had given us the fastest lap time but had factors like: model 2 had zero live training with only 1 hour of simulation training, along with the code not being as technical as model 3.

---

## Results  

The **stinkMobile** model achieved consistent lap times and excellent track adherence thanks to:  
- A dynamic **reward function** tuned for straightaways, curves, and steering control.  
- Continuous simulation feedback and real-world testing.  
- Effective teamwork and collaboration.  
---

## Lessons Learned
- **The Value of Iteration:**
Incremental changes to the reward function helped us address specific issues without introducing new ones.

- **Simulation Limitations:**
While simulations are valuable, real-world testing revealed nuances like traction loss and hardware constraints.

---

## Team Roles  

### Liam  
- **Setup and Training:** Configured AWS DeepRacer and initialized reward functions.  
- **Simulation Analysis:** Reviewed metrics and fine-tuned hyperparameters.  

### Nav  
- **Reward Function Optimization:** Collaborated on designing and refining reward strategies.  
- **Simulation Testing:** Documented tests and iteratively improved the model.  

### Mikayla  
- **Real-World Testing Lead:** Coordinated physical testing and adjustments.  
- **Race Strategy:** Designed final race strategies based on testing insights.  

---

## Resources (IEE)

- [Advanced Guide to AWS DeepRacer](https://towardsdatascience.com/an-advanced-guide-to-aws-deepracer-2b462c37eea)  
  *Techniques for reward function design, hyperparameter tuning, and physical testing.*  



---

 🚗💨  