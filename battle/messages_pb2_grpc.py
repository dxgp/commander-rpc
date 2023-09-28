# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import messages_pb2 as messages__pb2


class DefenseNotificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.launch_missile = channel.unary_unary(
                '/DefenseNotification/launch_missile',
                request_serializer=messages__pb2.missile_details.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )
        self.kill = channel.unary_unary(
                '/DefenseNotification/kill',
                request_serializer=messages__pb2.Empty.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )


class DefenseNotificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def launch_missile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def kill(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DefenseNotificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'launch_missile': grpc.unary_unary_rpc_method_handler(
                    servicer.launch_missile,
                    request_deserializer=messages__pb2.missile_details.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
            'kill': grpc.unary_unary_rpc_method_handler(
                    servicer.kill,
                    request_deserializer=messages__pb2.Empty.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DefenseNotification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DefenseNotification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def launch_missile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DefenseNotification/launch_missile',
            messages__pb2.missile_details.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def kill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DefenseNotification/kill',
            messages__pb2.Empty.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ControllerNotificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.missile_notification = channel.unary_unary(
                '/ControllerNotification/missile_notification',
                request_serializer=messages__pb2.missile_details.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )
        self.notify_controller = channel.unary_unary(
                '/ControllerNotification/notify_controller',
                request_serializer=messages__pb2.missile_details.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )


class ControllerNotificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def missile_notification(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def notify_controller(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ControllerNotificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'missile_notification': grpc.unary_unary_rpc_method_handler(
                    servicer.missile_notification,
                    request_deserializer=messages__pb2.missile_details.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
            'notify_controller': grpc.unary_unary_rpc_method_handler(
                    servicer.notify_controller,
                    request_deserializer=messages__pb2.missile_details.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ControllerNotification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ControllerNotification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def missile_notification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ControllerNotification/missile_notification',
            messages__pb2.missile_details.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def notify_controller(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ControllerNotification/notify_controller',
            messages__pb2.missile_details.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class SoldierNotificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.notify_soldier = channel.unary_unary(
                '/SoldierNotification/notify_soldier',
                request_serializer=messages__pb2.missile_details.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )
        self.soldier_status = channel.unary_unary(
                '/SoldierNotification/soldier_status',
                request_serializer=messages__pb2.Empty.SerializeToString,
                response_deserializer=messages__pb2.survival_response.FromString,
                )
        self.soldier_position = channel.unary_unary(
                '/SoldierNotification/soldier_position',
                request_serializer=messages__pb2.Empty.SerializeToString,
                response_deserializer=messages__pb2.position_details.FromString,
                )
        self.notify_commander = channel.unary_unary(
                '/SoldierNotification/notify_commander',
                request_serializer=messages__pb2.missile_details.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )
        self.make_commander = channel.unary_unary(
                '/SoldierNotification/make_commander',
                request_serializer=messages__pb2.Empty.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )
        self.kill = channel.unary_unary(
                '/SoldierNotification/kill',
                request_serializer=messages__pb2.Empty.SerializeToString,
                response_deserializer=messages__pb2.Empty.FromString,
                )


class SoldierNotificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def notify_soldier(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def soldier_status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def soldier_position(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def notify_commander(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def make_commander(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def kill(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SoldierNotificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'notify_soldier': grpc.unary_unary_rpc_method_handler(
                    servicer.notify_soldier,
                    request_deserializer=messages__pb2.missile_details.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
            'soldier_status': grpc.unary_unary_rpc_method_handler(
                    servicer.soldier_status,
                    request_deserializer=messages__pb2.Empty.FromString,
                    response_serializer=messages__pb2.survival_response.SerializeToString,
            ),
            'soldier_position': grpc.unary_unary_rpc_method_handler(
                    servicer.soldier_position,
                    request_deserializer=messages__pb2.Empty.FromString,
                    response_serializer=messages__pb2.position_details.SerializeToString,
            ),
            'notify_commander': grpc.unary_unary_rpc_method_handler(
                    servicer.notify_commander,
                    request_deserializer=messages__pb2.missile_details.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
            'make_commander': grpc.unary_unary_rpc_method_handler(
                    servicer.make_commander,
                    request_deserializer=messages__pb2.Empty.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
            'kill': grpc.unary_unary_rpc_method_handler(
                    servicer.kill,
                    request_deserializer=messages__pb2.Empty.FromString,
                    response_serializer=messages__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SoldierNotification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SoldierNotification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def notify_soldier(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierNotification/notify_soldier',
            messages__pb2.missile_details.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def soldier_status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierNotification/soldier_status',
            messages__pb2.Empty.SerializeToString,
            messages__pb2.survival_response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def soldier_position(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierNotification/soldier_position',
            messages__pb2.Empty.SerializeToString,
            messages__pb2.position_details.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def notify_commander(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierNotification/notify_commander',
            messages__pb2.missile_details.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def make_commander(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierNotification/make_commander',
            messages__pb2.Empty.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def kill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SoldierNotification/kill',
            messages__pb2.Empty.SerializeToString,
            messages__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
