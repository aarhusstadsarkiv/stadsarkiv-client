from stadsarkiv_client.core.templates import get_template_dirs
import os

"""
Read all icons from template dir
If a second template dir exists, override icons
This is only run once when the server starts
"""

template_dirs = get_template_dirs()

# if there is two template dirs, then first read second template dir
# and then add icons from first template dir if they are not set
# Path to icons is template_dir[0]/icons and template_dir[1]/icons
