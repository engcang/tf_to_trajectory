# Convert ROS messages to nav_msgs/Path to visualize in Rviz
+ `/tf` message to nav_msgs/Path
+ `geometry_msgs/PoseStamped` message to nav_msgs/Path
+ `gazebo_msgs/ModelStates` message to nav_msgs/Path
+ `nav_msgs/Odometry` message to nav_msgs/Path

<br><br>

### Execution
+ simply run
~~~shell
  $ roslaunch tf_to_trajectory tf_to_path.launch
  $ roslaunch tf_to_trajectory posestamped_to_path.launch
  $ roslaunch tf_to_trajectory gazebo_gt_to_path.launch
  $ roslaunch tf_to_trajectory odom_to_path.launch
~~~
+ Edit `parent frame id`, `child frame id`, and `topic name` in launch files
