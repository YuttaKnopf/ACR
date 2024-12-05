from enum import Enum


class Disruptions(Enum):
    SATURATION = "saturation"
    SMEAR = "smear"
    BLUR = "blur"
    SEWING = "sewing"
    CUT_IMAGE = "cut_image"
