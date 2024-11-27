

# AWS DeepRacer Hackathon  

The **AWS DeepRacer Hackathon** organized by the University of Victoria and Amazon, provided us with an excellent chance to examine **Reinforcement Learning (RL)** and apply it to real-world autonomous racing. Our project, **stinkMobile**, offers creative techniques to achieve efficient and consistent performance on both virtual and actual tracks.
---

## Event Overview  

AWS DeepRacer challenges students to train RL models in the cloud using **AWS DeepRacer virtual simulator** and deploy them on a 1/18th scale AI-powered car. The competition consisted of 5 hours worth of credits in simulation/virtual training time followed by physical track testing and  ending in a race day where all teams competed for the fastest lap time.  


## Our Approach  

### Reward Function  

The reward function is the foundation of our RL model, guiding the car during training. Our latest iteration incorporates a "stay left" strategy based on track characteristics, such as straightaways and curves, as well as penalties for excessive steering.  

```python
def reward_function(params):
    # Read input parameters
    track_width: float = params['track_width']
    distance_from_center: float = params['distance_from_center']
    left: bool = params["is_left_of_center"]
    on_track: bool = params["all_wheels_on_track"]
    abs_steering: float = abs(params['steering_angle'])  
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

2. **Stay left Strategy:**  
- Highest reward zone is in the 25-50% range left of the center line.  
- Higher penalties for straying too far from center line on the right.  

3. **Steering Control:**  
- A steering penalty prevents oversteering, improving lap consistency.  
---

### Strategies  

#### Simulation Training  

1. **Initial Testing:**  
- The model was trained using the **AWS DeepRacer virtual simulator**, providing valuable metrics like lap times and track completion rates.  

2. **Iterative Reward Function Refinement:**  
- Observed challenges, wide turns and steering inefficiencies, informed adjustments to the reward function.  

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
- The biggest challenge we ran into was with our reward function, where on testing day we observed our car model loved to go straight. Due to that fact the model car would have some difficulties in taking turns due to our reward function code as we wanted to reward our model car a good amount therefore the car taught it self to go straight more dominantly as we may have rewarded too many points.
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
- Configured AWS DeepRacer and initialized our model, worked on straightaway behaviour, and zig zag mitigation reward system.  
- Configured Git repository and managed team roles.
- Reviewed metrics and fine-tuned hyperparameters.  
- Implemented last minute Fixes to bug issues discovered on testin day.

### Nav  
- Collaborated on designing and refining reward strategies alongside the team.
- Worked on all documentation including code documentation and README.  
- Documented tests and iteratively improved the model.  

### Mikayla  
- Coordinated physical testing and adjustments, along with creating a zigzag function for our model.  
- Designed final race strategies based on testing insights.  
- Collaborated on Designing and Refining reward strategies.



---

## Resources (IEE)

- [Advanced Guide to AWS DeepRacer](https://towardsdatascience.com/an-advanced-guide-to-aws-deepracer-2b462c37eea)  
  *Techniques for reward function design, hyperparameter tuning, and physical testing.*  



---

 🚗💨  