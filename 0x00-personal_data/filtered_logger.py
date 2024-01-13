#!/usr/bin/env python3
'''Filtered logger module'''
import re


def filter_datum(fields: str, redaction: str, message: str, separator: str)\
        -> str:
    ''' Returns the log message obfuscated '''
    for field in fields:
        repl = field + "=" + redaction + separator
        obfuscated_message = re.sub(field + "=.*?" + separator, repl, message)
    return obfuscated_message
