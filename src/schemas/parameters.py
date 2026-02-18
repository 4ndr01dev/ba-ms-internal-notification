from typing import Literal

from pydantic import BaseModel


class Parameters(BaseModel):
    """
    Manages the validation of input parameters for the notification service.
    """

    ts_id: str
    type: Literal["operational", "satelite"]
