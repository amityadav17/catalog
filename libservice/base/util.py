import datetime
import re
from functools import reduce


def validate_email(email):
    """
    Performs validation of email address
    :param email:
        email address to verify
    :return:
        True, if email address matches the syntax
        False, if email address doesn't matches the syntax
    """

    email_syntax_match = re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

    if email_syntax_match is None:
        return False
    else:
        return True


def check_password(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 uppercase letter or more
    """

    # Length condition
    length_error = len(password) < 8

    # Digits condition
    digit_error = re.search(r'\d', password) is None

    # Uppercase condition
    uppercase_error = re.search(r'[A-Z]', password) is None

    # The check
    return not (length_error or digit_error or uppercase_error)


def get_datetime():
    """
    Get the current datetime

    :return: datetime object
    """
    return datetime.datetime.utcnow()


def datetime_to_string(date_time, use_time_output=True):
    """
    Convert datetime to standard formatted string

    :param date_time: The datetime object to convert
    :param use_time_output: Is string include time part
    :return: The resulting string
    """
    if use_time_output is True:
        output_date_format = "%Y-%m-%d %H:%M:%S"
    else:
        output_date_format = "%Y-%m-%d"

    return date_time.strftime(output_date_format)


def to_datetime(date_time_str, delay_if_too_late=None):
    """
    Convert any datetime string to datetime object

    :param date_time_str: String to parse
    :param delay_if_too_late: Get datetime of the same time tomorrow if we missed it today
    :return: The matching datetime object
    """
    # Split date and time
    m = re.match(r'([0-9]+-[0-9]+-[0-9]+)* *([0-9]+(:[0-9]+)*(:[0-9]+)*)*', date_time_str)
    if m.group(1) is None:
        date_str = str(datetime.datetime.utcnow().date())
    else:
        date_str = m.group(1)
    time_str = m.group(2) if len(m.groups()) > 1 and m.group(2) is not None else '00:00:00'

    # Pad time if required
    for i in range(0, 2 - time_str.count(':')):
        time_str += ':00'

    # Compute datetime
    date_time = datetime.datetime.strptime('{} {}'.format(date_str, time_str,), '%Y-%m-%d %H:%M:%S')

    if delay_if_too_late is not None and date_time < datetime.datetime.utcnow():
        date_time += delay_if_too_late

    return date_time


def deep_get(root_dict, *keys):
    """
    Perform deep search into nested dictionary.  This is more convenient than performing validation against None at each level.

    :param root_dict: root dictionary to search in
    :param keys: remaining parameters that are the keys to search
    :return: If one of the submitted keys isn't found, None is returned.  Otherwise, found value is returned.
    """
    return reduce(lambda d, key: d.get(key) if d else None, keys, root_dict)

    # for key in keys:
    #     if key in root_dict:
    #         root_dict = root_dict[key]
    #     else:
    #         return None
    # return root_dict
