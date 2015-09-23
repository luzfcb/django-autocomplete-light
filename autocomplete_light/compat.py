try:
    from django.apps import apps

    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

try:
    from django.utils.module_loading import import_string
except ImportError:
    from importlib import import_module
    from django.utils import six
    import sys

    # backport of https://github.com/django/django/blob/master/django/utils/module_loading.py#L9-L27 # noqa
    def import_string(dotted_path):
        """
        Import a dotted module path and return the attribute/class designated
        by the last name in the path. Raise ImportError if the import failed.
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            msg = "%s doesn't look like a module path" % dotted_path
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError:
            msg = 'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name)
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

__all__ = (
    'get_model',
    'import_string'
)
