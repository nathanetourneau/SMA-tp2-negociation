import scipy.stats as stats
import numpy as np


def gaussian(x: float):
    return stats.norm.pdf(x, 0.5, 0.4)
