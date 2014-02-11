# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('xpd54-cyberoam')

import logging
logger = logging.getLogger('xpd54_cyberoam')

from xpd54_cyberoam_lib.AboutDialog import AboutDialog

# See xpd54_cyberoam_lib.AboutDialog.py for more details about how this class works.
class AboutXpd54CyberoamDialog(AboutDialog):
    __gtype_name__ = "AboutXpd54CyberoamDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutXpd54CyberoamDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

