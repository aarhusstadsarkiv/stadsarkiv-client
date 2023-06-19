import pluggy  # type: ignore

hookimpl = pluggy.HookimplMarker("stadsarkiv_client")
"""Marker to be imported and used in plugins (and for own implementations)"""
