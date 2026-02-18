from typing import Annotated

import click
import typer

from .etl.extract import extract_data
from .etl.load import load_data
from .etl.transform import transform_data
from .schemas import Parameters
from .utils.logging import LOG_LEVELS, check_if_any_logger_is_below_level
from .utils.secrets import load_custom_dotenv


def main(
    arg_example: Annotated[
        str,
        typer.Option(
            help=(
                "This is an example argument. "
                "Delete it when you start developing your ETL."
            ),
        ),
    ] = "default",
    arg_ex_with_choices: Annotated[
        str,
        typer.Option(
            help=(
                "This is an example argument with choices. "
                "Delete it when you start developing your ETL."
            ),
            click_type=click.Choice(["choice1", "choice2", "choice3"]),
        ),
    ] = "choice1",
    max_level_logging: Annotated[
        str,
        typer.Option(
            "--max-level-logging",
            "-L",
            help=(
                "Maximum level of logging. "
                "Raises an error if any logger is below this level. "
                "Used in the development process to avoid setting the "
                "logging level to DEBUG."
            ),
            click_type=click.Choice(LOG_LEVELS),
        ),
    ] = "INFO",
):
    """
    Main function to run the ETL process.
    """

    # Load the dotenv file if load_dotenv is available.
    load_custom_dotenv()

    params = Parameters(
        arg_example=arg_example,
        arg_ex_with_choices=arg_ex_with_choices,
    )

    extracted_data = extract_data(params)
    transformed_data = transform_data(extracted_data, params)
    load_data(transformed_data, params)

    # Raise a warning if any logger is below the INFO level.
    if check_if_any_logger_is_below_level(max_level=max_level_logging):
        raise RuntimeError(
            f"Some logger is below the '{max_level_logging}' level"
        )


if __name__ == "__main__":
    typer.run(main)
