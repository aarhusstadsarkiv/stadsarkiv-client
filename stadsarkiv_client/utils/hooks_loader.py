from .dynamic_settings import get_setting

# print(get_setting("language"))

try:
    # import from current directory
    from plugins_test import test_test
    test_test()

    # from plugins_test import test_test
except ImportError:
    print("No plugins found")
    pass


# print(pm)
# test_test()
exit()

# call our `myhook` hook
results = pm.hook.before_render_template(arg1=1, arg2=2)
print(results)
