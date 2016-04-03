"""Useful utility functions for services."""

from datetime import datetime, timezone
import logging

from dateutil.parser import parse
from humanize import naturaldelta, naturaltime

logger = logging.getLogger(__name__)


def truncate(text, max_len=20):
    """Truncate the supplied text.

    Arguments:
      text (:py:class:`str`): The text to truncate.
      max_len (:py:class:`int`, optional): The maximum text length to
        return (defaults to ``20``).

    """
    if len(text) <= max_len:
        return text
    return '{}...'.format(text[:(max_len - 3)].strip())


def elapsed_time(start, end):
    """Calculate the elapsed time for a service activity.

    Arguments:
      start (:py:class:`str`): The activity start time.
      end (:py:class:`str`): The activity end time.

    Returns:
      :py:class:`str`: The humanized elapsed time.

    """
    try:
        return 'took {}'.format(naturaldelta(parse(end) - parse(start)))
    except (AttributeError, ValueError):
        logger.exception('failed to generate elapsed time')
    return 'elapsed time not available'


def occurred(at_):
    """Calculate when a service event occurred.

    Arguments:
      at_ (:py:class:`str`): When the event occurred.

    Returns:
      :py:class:`str`: The humanized occurrence time.

    """
    try:
        occurred_at = parse(at_)
    except (AttributeError, ValueError):
        logger.exception('failed to parse occurrence time')
        return 'time not available'
    utc_now = datetime.now(tz=timezone.utc)
    try:
        return naturaltime((utc_now - occurred_at).total_seconds())
    except TypeError:  # at_ is a naive datetime
        return naturaltime((datetime.now() - occurred_at).total_seconds())
