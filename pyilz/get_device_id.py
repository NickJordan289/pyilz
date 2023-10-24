try:
    import wmi
    import hashlib
    import pythoncom

    def get_device_id():
        '''
        Returns the unique device ID for this computer the same way the Unity game engine does. This allows us to interact with the game state without getting logged out.

        Currently only works on Windows.

        Returns:
            str: A SHA1 hash of the concatenated serial numbers of the Win32_BaseBoard, Win32_BIOS, and Win32_OperatingSystem WMI classes.
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
except:
    def get_device_id():
        return "default_device_id"


if __name__ == "__main__":
    print(get_device_id())
