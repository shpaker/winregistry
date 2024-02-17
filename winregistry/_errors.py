class WinRegistryError(
    ValueError,
):
    pass


class KeyNotFoundError(
    WinRegistryError,
):
    def __init__(
        self,
        path: str,
    ) -> None:
        super().__init__(f'Not found key in "{path}"')
