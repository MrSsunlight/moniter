#!usr/bin/env python
# -*- coding: utf-8 -*-

class Config:
    def load_config(self):
        print("========load_config=========")
        with open('./system.config', "r") as fd:

