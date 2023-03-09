import pluggy


hookspec = pluggy.HookspecMarker("stadsarkiv_client")


@hookspec
def before_render_template(context: dict):
    """Render context before the page is rendered.
    """
