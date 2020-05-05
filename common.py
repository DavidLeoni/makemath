import os
import io

out_path = 'out/'

errors_log_path = out_path + 'errors.log'

if not os.path.isdir(out_path):
    os.makedirs(out_path)

# let's disable the pointless file for now
f_errors = io.StringIO() # open(errors_log_path, 'w')    

log = {
        'warn' : [],
        'error' : [],
        'fatal' : []
    }


def format_log(msg=""):
    return "  %s" % msg

def fatal(msg, ex=None):
    """ Prints error and exits (halts program execution immediately)
    """
    if ex == None:
        exMsg = ""
    else:
        exMsg = " \n  " + repr(ex)
    s = format_log("\n\n    FATAL ERROR! %s%s\n\n" % (msg,exMsg))
    print(s)
    log['fatal'].append({'msg':s, 'ex':ex})
    f_errors.write(s)
    exit(1)

def log_error(msg, ex=None):
    """ Prints error but does not rethrow exception
    """
    if ex == None:
        exMsg = ""
        the_ex = Exception(msg)
    else:
        exMsg = " \n  " + repr(ex)
    the_ex = ex
    s = format_log("\n\n    ERROR! %s%s\n\n" % (msg,exMsg))
    print(s)
    log['error'].append({'msg':s, 'ex':ex})
    f_errors.write(s)

def error(msg, ex=None):
    """ Prints error and reraises Exception
    """
    log_error(msg, ex)
    if ex == None:
        exMsg = ""
    else:
        exMsg = " \n  " + repr(ex)
    if ex == None:
        raise Exception(exMsg)
    else:
        raise ex

def warn(msg, ex=None):
    if ex == None:
        exMsg = ""
    else:
        exMsg = " \n  " + repr(ex)

    s = format_log("\n\n   WARNING: %s%s\n\n" % (msg,exMsg))
    print(s)
    log['warn'].append({'msg':s, 'ex':ex})
    f_errors.write(s)

def info(msg=""):
    print(format_log(msg))

def debug(msg=""):
    print(format_log("  DEBUG=%s" % msg))
