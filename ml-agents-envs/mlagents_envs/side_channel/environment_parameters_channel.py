from mlagents_envs.side_channel import SideChannel, IncomingMessage, OutgoingMessage
from mlagents_envs.exception import UnityCommunicationException
import uuid
from enum import IntEnum
from typing import List


class EnvironmentParametersChannel(SideChannel):
    """
    This is the SideChannel for sending environment parameters to Unity.
    You can send parameters to an environment with the command
    set_float_parameter.
    """

    class EnvironmentDataTypes(IntEnum):
        FLOAT = 0
        SAMPLER = 1

    def __init__(self) -> None:
        channel_id = uuid.UUID(("534c891e-810f-11ea-a9d0-822485860400"))
        super().__init__(channel_id)

    def on_message_received(self, msg: IncomingMessage) -> None:
        raise UnityCommunicationException(
            "The EnvironmentParametersChannel received a message from Unity, "
            + "this should not have happend."
        )

    def set_float_parameter(self, key: str, value: float) -> None:
        """
        Sets a float environment parameter in the Unity Environment.
        :param key: The string identifier of the parameter.
        :param value: The float value of the parameter.
        """
        msg = OutgoingMessage()
        msg.write_string(key)
        msg.write_int32(self.EnvironmentDataTypes.FLOAT)
        msg.write_float32(value)
        super().queue_message_to_send(msg)

    def set_sampler_parameters(self, key: str, values: List[float]) -> None:
        """
        Sets a float encoding of an environment parameter sampelr.
        :param key: The string identifier of the parameter.
        :param value: The float encoding  of the sampler.
        """
        msg = OutgoingMessage()
        msg.write_string(key)
        msg.write_int32(self.EnvironmentDataTypes.SAMPLER)
        # length of list
        msg.write_int32(len(values))
        for value in values:
            msg.write_float32(value)
        super().queue_message_to_send(msg)
