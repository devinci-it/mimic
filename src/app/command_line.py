import argparse

class AbstractArgumentBuilder(type):
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        new_cls.parser = argparse.ArgumentParser(description="Execute Laravel Artisan command")
        return new_cls

class Argument:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.flag_name = None
        self.action_type = None

    def flag(self, flag_name):
        self.flag_name = flag_name
        return self

    def action(self, action_type):
        self.action_type = action_type
        return self

    def build(self, builder):
        builder.add_argument(*self.args, self.flag_name,
                             action=self.action_type)

class ArgumentBuilder(metaclass=AbstractArgumentBuilder):
    @classmethod
    def add_argument(cls, argument):
        argument.build(cls)

    @classmethod
    def add_common_flags(cls):
        cls.add_argument(
            Argument("-f", "--force", action="store_true", help="Force override files")
        )
        cls.add_argument(
            Argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
        )
        cls.add_argument(
            Argument("-d", "--destination", help="Destination directory with composer.json")
        )

    @classmethod
    def set_description(cls, description):
        cls.parser.description = description

    @classmethod
    def parse_arguments(cls):
        return cls.parser.parse_args()

# Example usage:
# ArgumentBuilder.set_description("Custom description for the argument parser")
