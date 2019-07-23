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
            config.number_of_rows_in_grid,
            config.number_of_columns_in_grid,
            config.fps,
            config.colour_rule,
            config.rule_set
        )

        # Run the display
        disp.run()
