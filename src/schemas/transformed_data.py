from pydantic import BaseModel


class TransformedData(BaseModel):
    """
    Manages the validation of transformed data so that it can be used by
    the loading functions.
    """

    # Define the structure of your transformed data here.
