"""
Defines common methods shared by Teams classes
"""
from __future__ import absolute_import, unicode_literals

from django.conf import settings

TEAM_DISCUSSION_CONTEXT = 'standalone'


def is_feature_enabled(course):
    """
    Returns True if the teams feature is enabled.
    """
    return settings.FEATURES.get('ENABLE_TEAMS', False) and course.teams_enabled
