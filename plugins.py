from stadsarkiv_client.utils.hooks_spec import plugin_manager, hookimpl


class Plugin_1:
    """A hook implementation namespace."""

    @hookimpl
    def before_render_template(self, arg1, arg2):
        print("inside Plugin_1.myhook()")
        return arg1 + arg2


class Plugin_2:
    """A 2nd hook implementation namespace."""

    @hookimpl
    def before_render_template(self, arg1, arg2):
        print("inside Plugin_2.myhook()")
        return arg1 - arg2


class Plugin_3:
    """A 3rd hook implementation namespace."""

    @hookimpl
    def before_render_template(self, arg1, arg2):
        print("inside Plugin_2.myhook()")
        return arg1 * arg2


plugin_manager.register(Plugin_1())
plugin_manager.register(Plugin_2())
plugin_manager.register(Plugin_3())
