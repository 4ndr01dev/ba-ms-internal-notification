from pydantic import BaseModel


class Parameters(BaseModel):
    """
    Manages the validation of ETL input parameters so that they can be used by
    the extraction, transformation, and loading functions.
    """

    # Some example parameters. Delete them when you start developing your ETL.
    arg_example: str
    arg_ex_with_choices: str
