from ctypes import windll
import win32api  # http://sourceforge.net/projects/pywin32/ -- Requires Python 3.5+
import win32clipboard  # http://sourceforge.net/projects/pywin32/
import msvcrt


def get_cursor():
    # Returns a tuple of x & y cursor pos
    return win32api.GetCursorPos()


def get_resolution():
    # Returns monitor height & width
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


def get_pixel_rgb(pixel_x, pixel_y):
    # Returns an RGB int which we convert out
    dc = windll.user32.GetDC(0)
    return rgb_convert(windll.gdi32.GetPixel(dc, pixel_x, pixel_y))


def rgb_convert(RGBInt):
    #  Basically only reading certain bytes of the integer for our RGB values
    blue = RGBInt & 255
    green = (RGBInt >> 8) & 255
    red = (RGBInt >> 16) & 255
    return red, green, blue


def set_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


def mouse_main():
    try:
        width, height = get_resolution()  # Retrieve the dimensions of the main monitor
        text_gui = f""" 
|---------------------------|
| Your monitor's resolution |
|---------------------------|
| Width x Height: {width}x{height} |
| Press F2 to copy the X/Y  |
| Press F3 to copy the RGB  |
|---------------------------|
Press Ctrl+C to quit."""
        windll.user32.SetProcessDPIAware()  # Make sure that windows scaling doesn't change our resolution
        print(text_gui)    
        last_xy = 'None'    
        last_rgb = 'None'    
        while True:    
            keyPress = None    
            if msvcrt.kbhit():    
                keyPress = msvcrt.getch()
            # Get and print the mouse coordinates.
            x, y = get_cursor()  # Tuple of current mouse position
            pixel_color = tuple(get_pixel_rgb(x, y))

            if keyPress == b'<':
                set_clipboard(f'({str(x)}, {str(y)})')
                last_xy = f'({str(x)}, {str(y)})'

            if keyPress == b'=':
                set_clipboard(f'{str(pixel_color)}')
                last_rgb = f'({str(pixel_color[0])}, {str(pixel_color[1])}, {str(pixel_color[2])})'
                last_rgb = get_pixel_rgb(x, y)

            position_str = f'X: {str(x).rjust(4)} Y: {str(y).rjust(4)} RGB: ({str(pixel_color[0]).rjust(3)},' \
                          f' {str(pixel_color[1]).rjust(3)}, {str(pixel_color[2]).rjust(3)}) |' \
                          f' Copied X/Y: {last_xy} | Copied RGB: {last_rgb}                    '
            print(position_str, end='')
            print('\b' * len(position_str) * 3, end='', flush=True)

    except KeyboardInterrupt:
        print("\nProgram ended...")

if __name__ == '__main__':
	mouse_main()
