from stadsarkiv_client.utils.hooks_spec import pm, hookimpl


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


pm.register(Plugin_1())
pm.register(Plugin_2())
pm.register(Plugin_3())


def test_test():
    print("Doh")


# print("Doh")
# call our `myhook` hook
""" results = pm.hook.before_render_template(arg1=1, arg2=2)
print(results) """
