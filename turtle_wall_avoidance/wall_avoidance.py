import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose

# The turtlesim window spans roughly 0 -> 11.09 on both axes
MIN_XY = 0.0
MAX_XY = 11.09
CENTRE = (MAX_XY / 2.0, MAX_XY / 2.0)
MARGIN = 1.5          # distance from a wall at which the turtle turns away
FORWARD_SPEED = 2.0
TURN_GAIN = 3.0


class WallAvoidanceNode(Node):
    def __init__(self):
        super().__init__('turtle_wall_avoidance')
        self.pose = None
        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(
            Pose, 'turtle1/pose', self.callback_turtle_bb_get_pose, 10)
        # Publish commands at 10 Hz using the latest pose
        self.timer = self.create_timer(0.1, self.control_loop)

    def callback_turtle_bb_get_pose(self, pose):
        self.pose = pose

    def near_wall(self, pose):
        return (pose.x < MIN_XY + MARGIN or pose.x > MAX_XY - MARGIN or
                pose.y < MIN_XY + MARGIN or pose.y > MAX_XY - MARGIN)

    @staticmethod
    def normalise(angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def control_loop(self):
        if self.pose is None:
            return  # no pose received yet

        msg = Twist()
        if self.near_wall(self.pose):
            # Steer towards the centre of the window (i.e. away from the walls)
            target = math.atan2(CENTRE[1] - self.pose.y, CENTRE[0] - self.pose.x)
            error = self.normalise(target - self.pose.theta)
            msg.angular.z = TURN_GAIN * error
            # Slow down while still facing the wall; speed up once facing away
            msg.linear.x = FORWARD_SPEED * max(0.0, math.cos(error)) * 0.5
        else:
            msg.linear.x = FORWARD_SPEED
            msg.angular.z = 0.0

        self.cmd_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = WallAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
