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
    env.tests.update(JinjaTest.salt_jinja_tests)


def load_filter_st2(env):
    pass