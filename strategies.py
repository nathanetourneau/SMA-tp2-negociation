import scipy.stats as stats
import numpy as np


def gaussienne(x: float):
    return stats.norm.pdf(x, 0.5, 0.4)

