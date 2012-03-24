#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def millisec(sec=None):
    """
    Return an integer representing current time in millisec since Unix epoch

    If the optional sec argument is given, converts that into millisec
    """
    return int(time.time() * 1000) if sec is None else int(sec * 1000)
