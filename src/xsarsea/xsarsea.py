__all__ = ["__version__", "cmodIfr2"]

import logging
from pkg_resources import get_distribution
import numpy as np

__version__ = get_distribution("xsarsea").version

logger = logging.getLogger("xsarsea")
logger.addHandler(logging.NullHandler())


def cmodIfr2(wind_speed, wind_dir, inc_angle):
    """get nrcs from wind speed, dir, and inc angle

    Parameters
    ----------
    wind_speed : float or numpy-like
        wind speed (m/s)
    wind_dir : float or numpy-like
        wind dir (deg)
    inc_angle : float or numpy-like
        inc angle (deg)

    Returns
    -------
    float or numpy-like
        simulated nrcs (linear)
    """
    # wind_speed = vent_fictif(wind_speed)

    C = np.zeros(26)

    # init CMOD-IFR2 coef
    C[0] = 0.0
    C[1] = -2.437597
    C[2] = -1.5670307
    C[3] = 0.3708242
    C[4] = -0.040590
    C[5] = 0.404678
    C[6] = 0.188397
    C[7] = -0.027262
    C[8] = 0.064650
    C[9] = 0.054500
    C[10] = 0.086350
    C[11] = 0.055100
    C[12] = -0.058450
    C[13] = -0.096100
    C[14] = 0.412754
    C[15] = 0.121785
    C[16] = -0.024333
    C[17] = 0.072163
    C[18] = -0.062954
    C[19] = 0.015958
    C[20] = -0.069514
    C[21] = -0.062945
    C[22] = 0.035538
    C[23] = 0.023049
    C[24] = 0.074654
    C[25] = -0.014713

    T = inc_angle
    wind = wind_speed

    tetai = (T - 36.0) / 19.0
    xSQ = tetai * tetai
    # P0 = 1.0
    P1 = tetai
    P2 = (3.0 * xSQ - 1.0) / 2.0
    P3 = (5.0 * xSQ - 3.0) * tetai / 2.0
    ALPH = C[1] + C[2] * P1 + C[3] * P2 + C[4] * P3
    BETA = C[5] + C[6] * P1 + C[7] * P2
    ang = wind_dir
    cosi = np.cos(np.deg2rad(ang))
    cos2i = 2.0 * cosi * cosi - 1.0
    tetamin = 18.0
    tetamax = 58.0
    tetanor = (2.0 * T - (tetamin + tetamax)) / (tetamax - tetamin)
    vmin = 3.0
    vmax = 25.0
    vitnor = (2.0 * wind - (vmax + vmin)) / (vmax - vmin)
    pv0 = 1.0
    pv1 = vitnor
    pv2 = 2 * vitnor * pv1 - pv0
    pv3 = 2 * vitnor * pv2 - pv1
    pt0 = 1.0
    pt1 = tetanor
    pt2 = 2 * tetanor * pt1 - pt0
    # pt3 = 2 * tetanor * pt2 - pt1
    b1 = C[8] + C[9] * pv1 \
        + (C[10] + C[11] * pv1) * pt1 \
        + (C[12] + C[13] * pv1) * pt2
    tetamin = 18.0
    tetamax = 58.0
    tetanor = (2.0 * T - (tetamin + tetamax)) / (tetamax - tetamin)
    vmin = 3.0
    vmax = 25.0
    vitnor = (2.0 * wind - (vmax + vmin)) / (vmax - vmin)
    pv0 = 1.0
    pv1 = vitnor
    pv2 = 2 * vitnor * pv1 - pv0
    pv3 = 2 * vitnor * pv2 - pv1
    pt0 = 1.0
    pt1 = tetanor
    pt2 = 2 * tetanor * pt1 - pt0
    # pt3 = 2 * tetanor * pt2 - pt1
    result = (
        C[14]
        + C[15] * pt1
        + C[16] * pt2
        + (C[17] + C[18] * pt1 + C[19] * pt2) * pv1
        + (C[20] + C[21] * pt1 + C[22] * pt2) * pv2
        + (C[23] + C[24] * pt1 + C[25] * pt2) * pv3
    )
    b2 = result

    b0 = np.power(10.0, (ALPH + BETA * np.sqrt(wind)))
    sig = b0 * (1.0 + b1 * cosi + np.tanh(b2) * cos2i)
    return sig
