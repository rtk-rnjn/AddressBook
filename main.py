from __future__ import annotations

import logging

from src import app

log = logging.getLogger()
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run()
