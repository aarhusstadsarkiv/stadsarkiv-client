import pluggy

hookspec = pluggy.HookspecMarker("myproject")
hookimpl = pluggy.HookimplMarker("myproject")


class MySpec:
    """A hook specification namespace."""

    @hookspec
    def before_render_template(self, arg1, arg2):
        """My special little hook that you can customize."""


# create a manager and add the spec
pm = pluggy.PluginManager("myproject")
pm.add_hookspecs(MySpec)
