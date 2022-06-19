# Parking a Car using Reinforcement Learning
- Parking a car using reinforcement learning
- Using benchmark: https://www.tpcap.net/#/

## MVP due June 30, 2022
- environment:
    - meets kinematic constraints of the competition
    - if car goes into an obstacle it dies
    - if the car's velocity is less than -2.5 or more than 2.5 it dies
    - if the car's steering angle is more than 0.75 or less than - 0.75 it dies
    - start with the first benchmark
- reward
    - how close its position is to the final position
    - ending
        - how close its steering angle is to the final position
        - TODO figure out later

## MVP for July 14
- repeat for all benchmarks
- output to csv as needed for competition

## Sprinkles
- optimize parameters with zoo
- One planner for all benchmarks
- streamlit demonstration in browser
- user can race against the ai to park
- user can add obstacles and then race
