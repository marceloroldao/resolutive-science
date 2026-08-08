"""Reference computational implementation for RCMS candidate models.

Scientific status: experimental implementation. This package does not imply
empirical validation of Resolutive Cosmology.
"""

from .background import LCDMParams, RCMSParams, h_lcdm, h_rcms_e020

__all__ = ["LCDMParams", "RCMSParams", "h_lcdm", "h_rcms_e020"]
