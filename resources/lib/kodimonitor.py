import xbmc

import os
import ui
import clientinfo

from tools import xbmclog
from ga_client import GoogleAnalytics

class KodiMonitor(xbmc.Monitor):

    hue_service = None
    ga = None

    def __init__(self):
        xbmclog('In KodiMonitor.__init__()')
        xbmc.Monitor.__init__(self)
        self.ga = GoogleAnalytics()

    def onSettingsChanged(self):
        xbmclog('In onSettingsChanged()')
        self.ga.sendScreenView("Configurations")
        self.hue_service.ga.sendEventData("Configurations", "Update")
        self.hue_service.settings.readxml()
        xbmclog("Updated settings: \n{}".format(self.hue_service.settings))
        self.hue_service.update_controllers()

    def onNotification(self, sender, method, data):
        xbmclog('In onNotification(sender={}, method={}, data={})'
                .format(sender, method, data))
        if sender == clientinfo.ClientInfo().get_addon_id():
            if 'discover' in method:
                self.ga.sendScreenView("Configurations/Discover")
                self.hue_service.ga.sendEventData("Configurations", "Discover")
                ui.discover_lights(self.hue_service)
                self.hue_service.update_controllers()
            if 'start_setup_theater_lights' in method:
                self.ga.sendScreenView("Configurations/SetupGroup/Theater")
                self.hue_service.ga.sendEventData("Configurations", "Setup Group", "Theater")
                ret = ui.multiselect_lights(
                    'Select Theater Lights',
                    ','.join([self.hue_service.settings.ambilight_group,
                              self.hue_service.settings.static_group]),
                    self.hue_service.settings.theater_group
                )
                self.hue_service.settings.update(theater_group=ret)
                self.hue_service.update_controllers()
            if 'start_setup_theater_subgroup' in method:
                self.ga.sendScreenView("Configurations/SetupGroup/TheaterSubgroup")
                self.hue_service.ga.sendEventData("Configurations", "Setup Group", "Theater Subgroup")
                ret = ui.multiselect_lights(
                    'Select Theater Subgroup',
                    ','.join([self.hue_service.settings.ambilight_group,
                              self.hue_service.settings.static_group]),
                    self.hue_service.settings.theater_subgroup
                )
                self.hue_service.settings.update(theater_subgroup=ret)
                self.hue_service.update_controllers()
            if 'start_setup_ambilight_lights' in method:
                self.ga.sendScreenView("Configurations/SetupGroup/Ambilight")
                self.hue_service.ga.sendEventData("Configurations", "Setup Group", "Ambilight")
                ret = ui.multiselect_lights(
                    'Select Ambilight Lights',
                    ','.join([self.hue_service.settings.theater_group,
                              self.hue_service.settings.static_group]),
                    self.hue_service.settings.ambilight_group
                )
                self.hue_service.settings.update(ambilight_group=ret)
                self.hue_service.update_controllers()
            if 'start_setup_static_lights' in method:
                self.ga.sendScreenView("Configurations/SetupGroup/Static")
                self.hue_service.ga.sendEventData("Configurations", "Setup Group", "Static")
                ret = ui.multiselect_lights(
                    'Select Static Lights',
                    ','.join([self.hue_service.settings.theater_group,
                              self.hue_service.settings.ambilight_group]),
                    self.hue_service.settings.static_group
                )
                self.hue_service.settings.update(static_group=ret)
                self.hue_service.update_controllers()
            if 'reset_settings' in method:
                self.ga.sendScreenView("Configurations/Reset")
                self.hue_service.ga.sendEventData("Configurations", "Reset")
                os.unlink(os.path.join(__addondir__, "settings.xml"))
