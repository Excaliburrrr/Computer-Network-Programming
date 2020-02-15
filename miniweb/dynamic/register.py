
URL_MODULE_DICT = dict()


def route(module_name):
    def register(module):
        URL_MODULE_DICT[module_name] = module

        def call_module(*args, **kwargs):
            return module(*args, **kwargs)
        return call_module

    return register


