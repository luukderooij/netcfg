from gui.main import launch_gui

import logging

if __name__ == "__main__":
    
    logging.basicConfig(
        level=logging.INFO,  # of DEBUG
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    launch_gui()
