#!/usr/bin/env python
# Import the neccesary modules
import sys
import os
import shutil
import frontend
import config

if __name__ == '__main__':
        # Set up the display
        disp = frontend.Display(
            config.numberOfRowsInGrid,
            config.numberOfColumnsInGrid,
            config.videoFPS,
            config.colourRule,
            config.ruleSet
        )

        # Run the display
        disp.run()
