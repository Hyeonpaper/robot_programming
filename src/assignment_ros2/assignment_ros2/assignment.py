import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from assignment_interfaces.msg import ID
from assignment_interfaces.srv import MultiplyTwoInts
from assignment_interfaces.action import AddID
from rclpy.action import CancelResponse, GoalResponse

class AssignmentNode(Node):
    def __init__(self):
        super().__init__('assignment_node')

        self.declare_parameter('university_id', '2020742057')
        self.declare_parameter('publish_frequency', 1.0)

        self.university_id = self.get_parameter('university_id').get_parameter_value().string_value
        publish_frequency = self.get_parameter('publish_frequency').get_parameter_value().double_value

        self.publisher_ = self.create_publisher(ID, 'university_id', 10)
        self.timer = self.create_timer(1.0 / publish_frequency, self.publish_id)

        self.srv = self.create_service(MultiplyTwoInts, 'multiply_two_ints', self.multiply_two_ints_callback)

        self._action_server = ActionServer(
            self,
            AddID,
            'add_id',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

    def publish_id(self):
        msg = ID()
        msg.id = self.university_id
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.id}')

    def multiply_two_ints_callback(self, request, response):
        response.product = request.a * request.b
        self.get_logger().info(f'Multiplying: {request.a} * {request.b} = {response.product}')
        return response

    def goal_callback(self, goal_request):
        self.get_logger().info(f'Received goal request: {goal_request.id}')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = AddID.Feedback()
        feedback_msg.partial_sum = []

        id_string = goal_handle.request.id
        intermediate_result = 0

        for digit in id_string:
            intermediate_result += int(digit)
            feedback_msg.partial_sum.append(intermediate_result)
            self.get_logger().info(f'Publishing feedback: {feedback_msg.partial_sum}')
            goal_handle.publish_feedback(feedback_msg)

        result = AddID.Result()
        result.result_sequence = feedback_msg.partial_sum

        self.get_logger().info('Goal succeeded')
        goal_handle.succeed()
        goal_handle.result = result

        return result

def main(args=None):
    rclpy.init(args=args)
    node = AssignmentNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()   