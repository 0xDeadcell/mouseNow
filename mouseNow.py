from ctypes import windll
import win32api
import win32clipboard  # http://sourceforge.net/projects/pywin32/
import msvcrt


def getCursor():
    # Returns a tuple of x & y cursor pos
    return win32api.GetCursorPos()


def getResolution():
    # Returns monitor height & width
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


def getPixelRGB(pixel_x, pixel_y):
    # Returns an RGB int which we convert out
    dc = windll.user32.GetDC(0)
    return RGBConvert(windll.gdi32.GetPixel(dc, pixel_x, pixel_y))


def RGBConvert(RGBInt):
    #  Basically only reading certain bytes of the integer for our RGB values
    blue = RGBInt & 255
    green = (RGBInt >> 8) & 255
    red = (RGBInt >> 16) & 255
    return red, green, blue


def setClipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


windll.user32.SetProcessDPIAware()  # Make sure that windows scaling doesn't change our resolution
width, height = getResolution()  # Retrieve the dimensions of the main monitor


print(f""" 
|---------------------------|
| Your monitor's resolution |
|---------------------------|
| Width x Height: {width}x{height} |
| Press F2 to copy the X/Y  |
| Press F3 to copy the RGB  |
|---------------------------|
Press Ctrl+C to quit.""")

try:
    last_xy = 'None'
    last_rgb = 'None'
    while True:
        keyPress = None
        if msvcrt.kbhit():
            keyPress = msvcrt.getch()
        # Get and print the mouse coordinates.
        x, y = getCursor()  # Tuple of current mouse position
        pixelColor = tuple(getPixelRGB(x, y))

        if keyPress == b'<':
            setClipboard(f'({str(x)}, {str(y)})')
            last_xy = f'({str(x)}, {str(y)})'

        if keyPress == b'=':
            setClipboard(f'{str(pixelColor)}')
            last_rgb = f'({str(pixelColor[0])}, {str(pixelColor[1])}, {str(pixelColor[2])})'
            last_rgb = getPixelRGB(x, y)

        positionStr = f'X: {str(x).rjust(4)} Y: {str(y).rjust(4)} RGB: ({str(pixelColor[0]).rjust(3)},' \
                      f' {str(pixelColor[1]).rjust(3)}, {str(pixelColor[2]).rjust(3)}) |' \
                      f' Copied X/Y: {last_xy} | Copied RGB: {last_rgb}                    '
        print(positionStr, end='')
        print('\b' * len(positionStr) * 3, end='', flush=True)

except KeyboardInterrupt:
    print("\nProgram ended...")
