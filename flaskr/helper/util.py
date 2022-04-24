import re
import uuid


def validate_string(str_input):
    return re.match("(^[_\\-\\.0-9a-z]{1,127}$)", str_input) != None


def validate_num(num_input):
    return re.match("^([1-9][0-9]*|0)(\.[0-9]{2})$", num_input) != None

def create_random_userid():
    return str(uuid.uuid4())
