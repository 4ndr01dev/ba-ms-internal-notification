from typing import Annotated, Literal

import click
import typer

from .schemas import Parameters
from .service.notify import dummy_notify
from .utils.logging import LOG_LEVELS, check_if_any_logger_is_below_level
from .utils.secrets import load_custom_dotenv


def main(
    ts_id: Annotated[
        str,
        typer.Option(
            help="Time series identifier to process.",
        ),
    ],
    type: Annotated[
        Literal["operational", "satelite"],
        typer.Option(
            help="Type of time series (operational or satelite).",
            click_type=click.Choice(["operational", "satelite"]),
        ),
    ],
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
    Main function to run the dummy notification process.
    """

    # Load the dotenv file if load_dotenv is available.
    load_custom_dotenv()

    params = Parameters(ts_id=ts_id, type=type)

    # Dummy execution: only print to console
    dummy_notify()

    # Raise a warning if any logger is below the INFO level.
    if check_if_any_logger_is_below_level(max_level=max_level_logging):
        raise RuntimeError(
            f"Some logger is below the '{max_level_logging}' level"
        )


if __name__ == "__main__":
    typer.run(main)
