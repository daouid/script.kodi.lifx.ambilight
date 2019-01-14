import os
import xbmcgui

TESTING_ENV = False

try:
    import xbmc
    import xbmcaddon

    __addon__ = xbmcaddon.Addon()
    __cwd__ = __addon__.getAddonInfo('path')
    __icon__ = os.path.join(__cwd__, "resources/icon.png")
    
except ImportError:
    TESTING_ENV = True


def xbmclog(message, level=None):
    if TESTING_ENV:
        pass
    else:
        level = xbmc.LOGDEBUG if level is None else level
        xbmc.log("Kodi Lifx: %s" % message, level=level)

def notify(title, msg=''):
    if TESTING_ENV:
        pass
    else:
        xbmc.executebuiltin('XBMC.Notification({}, {}, 3, {})'.format(
            title, msg, __icon__))

pDialog = None

def show_busy_dialog():
    # pass
    # TODO - add timeout thread to close the dialog
    xbmc.executebuiltin('ActivateWindow(busydialog)')
    # pDialog = xbmcgui.DialogProgressBG()
    # pDialog.create('Kodi Lifx', 'Processing your request...')

def hide_busy_dialog():
    # pass
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    while xbmc.getCondVisibility('Window.IsActive(busydialog)'):
        xbmc.sleep(100)
    # if pDialog:
    #     pDialog.update(100, message='Done')
    #     pDialog.close()
