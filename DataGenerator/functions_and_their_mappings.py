import random
from random import randint
import string
import datetime


def varchar_returner(max_length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=randint(1, max_length)))


def smallint_returner():
    return random.uniform(-32768, 32767)


def integer_returner():
    return random.uniform(-2147483648, 2147483647)


def bigint_returner():
    return random.uniform(-9223372036854775808, 9223372036854775807)


def numeric_returner(precision, scale):
    value = random.uniform(10**(precision-1), 10**(precision)-1)
    scale = 10**scale
    value = value/scale
    return value


def date_returner():
    return datetime.datetime(randint(1970, 2018), randint(1, 12), randint(1, 28))


def boolean_returner():
    return bool(random.getrandbits(1))


def timestamp_returner():
    return datetime.datetime.strptime('{} {}'.format(random.randint(1,366),random.randint(1970,2018)),'%j %Y')


no_argument_functions = {
    "SMALLINT": smallint_returner,
    "INT2": smallint_returner,

    "INTEGER": integer_returner,
    "INT": integer_returner,
    "INT4": integer_returner,

    "BIGINT": bigint_returner,
    "INT8": bigint_returner,

    "REAL": "",
    "FLOAT4": "",

    "DOUBLE PRECISION": "",
    "FLOAT8": "",

    "BOOLEAN": boolean_returner,
    "BOOL": boolean_returner,

    "DATE": date_returner,

    "DATETIME": timestamp_returner,
    "TIMESTAMP": timestamp_returner,
    "TIMESTAMP WITHOUT TIME ZONE": timestamp_returner,
    "TIMESTAMPTZ": timestamp_returner,
    "TIMESTAMP WITH TIME ZONE": timestamp_returner
}

one_argument_functions = {
        "CHAR": varchar_returner,
        "CHARACTER": varchar_returner,
        "NCHAR": varchar_returner,
        "BPCHAR": varchar_returner,

        "VARCHAR": varchar_returner,
        "CHARACTER VARYING": varchar_returner,
        "NVARCHAR": varchar_returner,
        "TEXT": varchar_returner
}

two_arguments_functions = {
        "DECIMAL": numeric_returner,
        "NUMERIC": numeric_returner
}