"""Useful utility functions for services."""

from humanize import naturaldelta


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
      start (:py:class:`datetime.datetime`): The activity start time.
      end (:py:class:`datetime.datetime`): The activity end time.

    Returns:
      :py:class:`str`: The humanized elapsed time.

    """
    return 'Took {}'.format(naturaldelta(end - start))
