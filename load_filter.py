def load_filter_ansible(env):
    from ansible.plugins.loader import filter_loader, test_loader

    for fp in filter_loader.all():
        env.filters.update(fp.filters())
    for fp in test_loader.all():
        env.tests.update(fp.tests())


def load_filter_salt(env):
    from salt.utils import templates
    from salt.utils.decorators.jinja import JinjaFilter, JinjaTest

    env.filters.update(JinjaFilter.salt_jinja_filters)
    env.filters["http_query"] = lambda *args, **kwargs: "http_query disabled"
    env.filters["method_call"] = lambda *args, **kwargs: "method_call disabled"
    env.filters["dns_check"] = lambda *args, **kwargs: "dns_check disabled"

    env.tests.update(JinjaTest.salt_jinja_tests)


def load_filter_st2(env):
    from st2common.util.jinja import get_filters

    env.filters.update(get_filters())
    # https://github.com/StackStorm/st2/blob/master/st2common/st2common/util/jinja.py#L110
    env.tests["in"] = lambda item, list: item in list
