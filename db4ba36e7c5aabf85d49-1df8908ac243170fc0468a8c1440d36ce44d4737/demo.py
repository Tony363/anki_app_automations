#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 17:24:35 2021

@author: pysolver33
"""

from anki_export import ApkgReader
import pyexcel_xlsxwx

with ApkgReader('../Selected-Notes4.apkg') as apkg:
    pyexcel_xlsxwx.save_data('test.xlsx', apkg.export(), config={'format': None})
