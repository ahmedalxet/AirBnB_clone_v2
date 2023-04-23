#!/usr/bin/env python3
"""
This module contains a Fabric script that generates a .tgz archive from the
contents of the web_static folder of your AirBnB Clone repo, using the function
do_pack.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Archives the web_static folder into a .tgz file.

    Returns:
        Path of the archive file if successful, None otherwise.
    """
    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Create the archive file name with the current timestamp
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(now)

    # Archive the web_static folder into the archive file
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # If the archive was created successfully, return its path; otherwise, return None
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None
