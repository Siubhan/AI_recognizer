from wx import DisplaySize

B_SIZE = (200, 30)


def get_measurement():
    user_width, user_height = DisplaySize()

    __standart_width, __standart_height = 1920, 1080
    __WIDTH = int(__standart_width / (user_width / 700))
    __HEIGHT = int(__standart_height / (user_height / 500))

    __scale_factor = ((__HEIGHT + __WIDTH) / 15) / 100
    __FONT_SIZE = int(14 * __scale_factor)

    return __WIDTH, __HEIGHT, __FONT_SIZE


def is_double(event):
    key_code = event.GetKeyCode()

    if chr(key_code).isnumeric() or chr(key_code) == '.':
        event.Skip()
        return

    return


def is_char(event):
    key_code = event.GetKeyCode()
    if len(event.GetEventObject().GetValue()) == 32:
        return

    if chr(key_code).isalpha() or chr(key_code) == '-':
        event.Skip()
        return

    return


def is_numbers(event):
    key_code = event.GetKeyCode()
    if chr(key_code).isnumeric() or chr(key_code) == '-':
        event.Skip()
        return

    return


def is_digit(event):
    key_code = event.GetKeyCode()
    if chr(key_code).isnumeric():
        event.Skip()
        return
    return


def is_mail(event):
    key_code = event.GetKeyCode()
    if key_code < 255:
        if chr(key_code).isalnum() or chr(key_code) == '-' or chr(key_code) == '@' or chr(key_code) == '.':
            event.Skip()
            return
    return
