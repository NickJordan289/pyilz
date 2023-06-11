import wmi
import hashlib
import pythoncom


def get_device_id():
    '''Returns the unique device ID for this computer the same way the Unity game engine does. This allows us to interact with the game state without getting logged out.

    Currently only works on Windows.
    '''
    # Use CoInitialize to avoid errors like this:
    #    http://stackoverflow.com/questions/14428707/python-function-is-unable-to-run-in-new-thread
    pythoncom.CoInitialize()
    c = wmi.WMI()
    s = ""
    for item in c.query("SELECT * FROM Win32_BaseBoard"):
        s += item.SerialNumber
    for item in c.query("SELECT * FROM Win32_BIOS"):
        s += item.SerialNumber
    for item in c.query("SELECT * FROM Win32_OperatingSystem"):
        s += item.SerialNumber
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    print(get_device_id())
