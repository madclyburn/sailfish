"""
Utility functions to facilitate consistent logging and terminal reporting
"""
from sys import stdout


def configure_logger(logger, log_level="success"):
    """
    Configure loguru logger object for application-level use

    This function clears any existing logger configuration. It adds two sinks:
    one to carry machine-readable messages logged from application internals
    (level=`log_level`), and another to print human-readable help and
    documentation messages to the terminal (level="TERM"). Both sinks are set to
    stdout, for now.

    Messages to the terminal should be emitted through the function returned by
    the `terminal` function below.

    WARNING: This function should only be called once (calling again will
    cause the logger.level function to fail).
    """
    log_format = (
        "<blue><b>{elapsed}</b></blue>:"
        "<level>{level: <8}</level>"
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger.remove()
    logger.level("TERM", 0)
    logger.add(
        stdout,
        level=log_level.upper(),
        format=log_format,
        filter=lambda r: r["level"].name != "TERM",
    )
    logger.add(
        stdout,
        level="TERM",
        format="{message}",
        filter=lambda r: r["level"].name == "TERM",
    )


def iteration_msg(iter: int, time: float, zps: float):
    """
    Return a string formatted for a reasonable iteration message.

    Parameters
    ----------

    iter: Iteration number
    time: Simulation time
    zps:  Zone-updates per second
    """
    return (
        f"<blue><b>{iter:04d}</b></blue> "
        f"<red>time</red>:{time:.4f} "
        f"<red>Mzps</red>:{zps/1e6:.3f}"
    )


def terminal(logger, ansi=True):
    """
    Return a function which logs at the TERM level.
    """
    return lambda msg: logger.opt(ansi=ansi).log("TERM", msg)


def add_logging_arguments(parser):
    """
    Add parser arguments to control logging and reporting

    Currently this function only adds the --log-level argument to the parser.
    """
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["trace", "debug", "info", "success", "warning", "error", "critical"],
        help="log messages at and above this severity level",
    )
