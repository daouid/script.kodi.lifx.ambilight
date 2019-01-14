import math

from tools import xbmclog


def transition_colorspace(hue, light, hsvratio):
    h, s, v = hsvratio.hue(
        hue.settings.ambilight_min, hue.settings.ambilight_max
    )
    if light.hue is None:
        light.hue = 1
    hvec = abs(h - light.hue) % int(65535/2)
    hvec = float(hvec/128.0)
    if light.sat is None:
        light.sat = 1
    svec = s - light.sat
    vvec = v - light.bri
    # changed to squares for performance
    distance = math.sqrt(hvec**2 + svec**2 + vvec**2)
    xbmclog('transition_colorspace {} {} {}'.format(light, hsvratio, distance))
    if distance > 0:
        # Old algorithm
        # duration = int(3 + 27 * distance/255)
        # New algorithm
        duration = int(10 - 2.5 * distance/255)
        if not hue.settings.force_light_on and not light.init_on:
            return
        light.set_state(hue=h, sat=s, bri=v, kel=None, transition_time=duration)

def transition_colorspacen(hue, light, hsvratios):
    def hs(i, hsvratio):
        h, s, v = hsvratio.hue(
            hue.settings.ambilight_min, hue.settings.ambilight_max
        )
        if light.hue is None:
            light.hue = [1] * light.num_zones
        hvec = abs(h - light.hue[i]) % int(65535/2)
        hvec = float(hvec/128.0)
        if light.sat is None:
            light.sat = [1] * light.num_zones
        svec = s - light.sat[i]
        vvec = v - light.bri[i]
        # changed to squares for performance
        distance = math.sqrt(hvec**2 + svec**2 + vvec**2)
        return h, s, v, distance

    values = [hs(i, hsvratio) for i, hsvratio in enumerate(hsvratios)]
    distance = max([v[3] for v in values])
    xbmclog('transition_colorspacen {} {} {}'.format(light, hsvratios, distance))
    if distance > 0:
        # Old algorithm
        # duration = int(3 + 27 * distance/255)
        # New algorithm
        duration = int(10 - 2.5 * distance/255)
        if not hue.settings.force_light_on and not light.init_on:
            return
        light.set_state(
            hue=[v[0] for v in values],
            sat=[v[1] for v in values],
            bri=[v[2] for v in values],
            kel=None,
            transition_time=duration)
