#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib import biplist
import os
import json
import sys
from workflow import Workflow3, ICON_WARNING, MATCH_SUBSTRING

def read_profiles():
    # Read iTerm's preferences file
    iTermPreferencesPath = os.path.join(os.environ["HOME"], "Library",
                                        "Preferences",
                                        "com.googlecode.iterm2.plist")

    plist = biplist.readPlist(iTermPreferencesPath)
    # Extract profile data from plist
    profiles = []
    for nb in plist['New Bookmarks']:
        tags = " ".join(nb.get('Tags'))
        profiles.append({
            'name': nb.get('Name'),
            'command': nb.get('Command'),
            'icon': nb.get('Custom Icon Path'),
            'tags': tags
        })

    return profiles


def filter_key_for_profile(profile):
    return profile['name'] + profile['tags']


def sort_key_for_profile(profile):
    return profile['name'] + profile['tags']


def main(wf):
    profiles = wf.cached_data('profiles', read_profiles, max_age=30)

    # Query argument Ensure `query` is initialised
    query = None
    if len(wf.args):
        query = wf.args[0]

    profiles = wf.filter(query, profiles, filter_key_for_profile,
                         match_on=MATCH_SUBSTRING)

    if not profiles:
        wf.add_item('No profile matches', icon=ICON_WARNING)
    else:
        profiles.sort(key=sort_key_for_profile)
        for profile in profiles:
            wf.add_item(title=profile['name'],
                        subtitle=(profile['tags'] if profile['tags'] else '') + profile['command'],
                        arg=profile['name'],
                        valid=True,
                        icon=profile['icon'])
    wf.send_feedback()
    return


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
