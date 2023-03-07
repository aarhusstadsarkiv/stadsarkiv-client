import pluggy


hookspec = pluggy.HookspecMarker("stadsarkiv_client")


@hookspec
def before_render_template():
    """Render context before the page is rendered.
    """
