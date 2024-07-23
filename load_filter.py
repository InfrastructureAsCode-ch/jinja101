import sysconfig
from pathlib import Path

def load_filter_ansible(env):
    from ansible.plugins.loader import filter_loader, test_loader

    for path in [
        str(x.resolve())
        for x in Path(
            f"{sysconfig.get_path('purelib')}/ansible_collections/").glob(
            "**/plugins/filter")
        if "tests" not in str(x)
    ]:
        filter_loader.add_directory(path)

    for fp in filter_loader.all():
        filter_name = fp._load_name
        filter = fp.j2_function
        path_parts = fp._original_path.split("/")
        site_packages = path_parts.index("site-packages")

        if path_parts[site_packages : site_packages + 2] == [
            "site-packages",
            "ansible",
        ]:
            env.filters[f"ansible.builtin.{filter_name}"] = filter
            env.filters[filter_name] = filter
        else:
            if path_parts[site_packages + 2 : -3] == [
                "community",
                "general",
            ] or path_parts[site_packages + 2 : -3] == ["ansible", "netcommon"]:
                env.filters[filter_name] = filter
            filter_name = ".".join(
                path_parts[site_packages + 2 : -3] + [filter_name]
            )
            env.filters[filter_name] = filter

    for fp in test_loader.all():
        env.tests.update({fp.ansible_name: fp._function})


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
