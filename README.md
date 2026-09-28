# TurtleSim Wall Avoidance

A ROS2 (Python) node that keeps the turtlesim turtle away from the walls.

- Subscribes to turtle1/pose to read the turtle's x and y position
- Publishes velocity commands to turtle1/cmd_vel
- When the turtle gets within 1.5 units of a wall, it turns back toward the centre

To run it, start turtlesim in one terminal:

    ros2 run turtlesim turtlesim_node

Then run the node in a second terminal:

    ros2 run turtle_wall_avoidance wall_avoidance
