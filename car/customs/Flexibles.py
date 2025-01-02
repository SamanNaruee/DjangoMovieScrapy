import os, sys

def custom_log(value, message=''):
    """
    print out in terminal value with message.
    args:
        value, message: default ''.
    out:
        file and its path, massage, value(s).
    """
    
    caller_frame = sys._getframe().f_back
    print("##############################")
    print(message)
    print(f"Your value:\n{value}")
    print(f"File path: {os.path.abspath(caller_frame.f_code.co_filename)}")
    print(f"Function name: {caller_frame.f_code.co_name}")
    print("\n##############################")
