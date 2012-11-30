# coding=utf-8
# See /usr/include/sysexits.h
EX_OK = 0
EX_USAGE = 64
EX_DATAERR = 65
EX_NOUSER = 67
EX_PROTOCOL = 76
EX_TEMPFAIL = 75
EX_CONFIG = 78
exit_vals = {
    'success': EX_OK,
    'input_file_empty': EX_DATAERR,
    'input_file_too_large': EX_DATAERR,
    'config_error': EX_CONFIG,
    'url_bung': EX_USAGE,
    'communication_failure': EX_PROTOCOL,
    'socket_error': EX_PROTOCOL,
    'locked': EX_TEMPFAIL,  # Postfix will try again later
    'no_x_original_to': EX_DATAERR,
    'json_decode_error': EX_PROTOCOL,
    'no_group': EX_NOUSER, }
