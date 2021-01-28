# Pathfinding Algorithms with Mazes

### <u>Current Working Algorithms:</u>

- A* optimised
  - As opposed to brute forcing each available path the program finds nodes

  - This can reduce total working area by a significant amount

  - 4k x 4k (16 million pixels) Mazes with multiple solutions can take under a minute to solve on basic hardware

  - It is not optimised to work with multiple threads


####  Special thanks to [MikePound](https://github.com/mikepound/mazesolving), I used a few of his mazes and ideas from [Computerphile](https://www.youtube.com/watch?v=rop0W4QDOUI) to get going!
### Demonstration  

## Maze (41x41)

![Maze](https://user-images.githubusercontent.com/20164942/106104104-69360c00-615b-11eb-9b8c-003238b913d4.png)

## Finding nodes:

![Terminal](https://user-images.githubusercontent.com/20164942/106104447-e2cdfa00-615b-11eb-8c05-6b53c626c25d.png)


![Maze Node](https://user-images.githubusercontent.com/20164942/106104028-4572c600-615b-11eb-9b76-ad13b59d3687.png)

## Solved:
![image](https://user-images.githubusercontent.com/20164942/106104604-19a41000-615c-11eb-835a-0281f8b86085.png)

![image](https://user-images.githubusercontent.com/20164942/106104222-94206000-615b-11eb-9d28-89673c4ee90a.png)


#### Additional Solved mazes can be found in the solved folder

- Notes:
  - Larger mazes example
  - 4 million pixel width
  - ![image](https://user-images.githubusercontent.com/20164942/106104985-ab138200-615c-11eb-8b06-2206b02d3802.png)
  - Trimmed to nearly 600k (~85% reduction) 
  - Node discovery is approx 75k/s (on an older laptop, yet to test on others)
  - Started at ~12.5k/s initally (500% increase)


## Additonal mazes:
#### 400x100
![400x100](./Solved/400x100_solved.png)

#### 200x200
![200x200](./Solved/200x200_solved.png)

#### Computerphile
![400x100](./Solved/computerphile_solved.png)
