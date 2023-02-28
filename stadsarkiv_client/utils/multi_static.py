import typing
from starlette.staticfiles import PathLike, StaticFiles

# Override static files in order to load multiple static folders
# https://github.com/encode/starlette/issues/537
class MultiStaticFiles(StaticFiles):
    def __init__(self, directories: typing.List[PathLike] = [], **kwargs) -> None:
        super().__init__(**kwargs)
        self.all_directories = self.all_directories + directories