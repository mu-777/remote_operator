#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Joy
from remote_ope.msg import RemoteCommand, RemoteCommands

# param-able
ROBOT_NUM = 10
# remap-able
NODE_NAME = 'remote_operator'
REMOTE_COMMAND_TOPIC_NAME = 'remote_commands'
JOY_TOPIC_NAME = 'joy'


class RemoteOperator(object):
    def __init__(self):

        self._robot_num = rospy.get_param('~robot_num', ROBOT_NUM)
        self._pub_remote_commands = rospy.Publisher(REMOTE_COMMAND_TOPIC_NAME, RemoteCommands, queue_size=1)
        self._remote_commands = RemoteCommands()
        self.is_active = False

        self._initialize_data()

    def _initialize_data(self):
        for idx in range(self._robot_num):
            self._remote_commands.list.append(RemoteCommand())

    def activate(self):
        rospy.Subscriber(JOY_TOPIC_NAME, Joy, self._joy_callback)
        self.is_active = True

    def _joy_callback(self, joy_data):
        remote_control_flag = False
        v = 0.0
        w = 0.0
        for idx in range(self._robot_num):
            self._remote_commands.list[idx].id = idx + 1
            self._remote_commands.list[idx].is_remote_controlled = remote_control_flag
            self._remote_commands.list[idx].v = v
            self._remote_commands.list[idx].w = w

    def publish_data(self):
        if not self.is_active:
            self.activate()
        self._pub_remote_commands.publish(self._remote_commands)


# --------------------------------------------
if __name__ == '__main__':
    rospy.init_node(NODE_NAME, anonymous=True)
    rate_mgr = rospy.Rate(30)  # Hz

    remote_operator = RemoteOperator()
    remote_operator.activate()

    while not rospy.is_shutdown():
        remote_operator.publish_data()
        rate_mgr.sleep()



