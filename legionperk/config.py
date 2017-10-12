#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
#******************************************************************************
#********************* Carbyne Solutions, Incorporated ************************
#------------------------------------------------------------------------------
#
# [2014] - [2014] Carbyne Solutions, Incorporated
# All Rights Reserved
#
# Notice: All information contained herein is, and remains the property of
# Carbyne Solutions, Incorporated and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Carbyne Solutions
# Incorporated and its suppliers, if any, and may be covered by U.S and Foreign
# Patents, patents in process, and are protected by trade secret or copyright
# law. Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from Carbyne
# Solutions, Incorporated.
#
#******************************************************************************

import yaml


def parse(filename):
    """Parse a yaml config file.

    :param filename: a filename / filepath
    :returns: dict. a parsed configuration object
    """
    with open(filename) as fptr:
        data = yaml.load(fptr.read())
    return data