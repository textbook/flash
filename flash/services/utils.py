"""Useful utility functions for services."""

from datetime import datetime, timezone
import logging
import re

from dateutil.parser import parse
from humanize import naturaldelta, naturaltime

logger = logging.getLogger(__name__)

WORDS = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
         '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten'}

NUMBERS = re.compile(r'\b([1-9]|10)\b')


def _numeric_words(text):
    """Replace numbers 1-10 with words.

    Arguments:
      text (:py:class:`str`): The text to replace numbers in.

    Returns:
      :py:class:`str`: The new text containing words.

    """
    return NUMBERS.sub(lambda m: WORDS[m.group()], text)


def friendlier(func):
    """Replace numbers to make functions friendlier.

    Arguments:
      func: The function to wrap.

    Returns:
      A wrapper function applying :py:func:`_numeric_words`.

    """
    def wrapper(*args, **kwargs):
        """Wrapper function to apply _numeric_words."""
        result = func(*args, **kwargs)
        try:
            return _numeric_words(result)
        except TypeError:
            return result
    return wrapper

naturaldelta = friendlier(naturaldelta)
naturaltime = friendlier(naturaltime)


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
