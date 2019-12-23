"""
Experimentation routers
"""
from __future__ import absolute_import

from rest_framework import routers
from rest_framework.routers import DynamicRoute, Route


class DefaultRouter(routers.DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                # Allow PUT as create
                'put': 'create_or_update',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            name='{basename}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            name='{basename}',
            detail=True,
            initkwargs={}
        ),
    ]
