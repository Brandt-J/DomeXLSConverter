from dataclasses import dataclass


@dataclass
class TableItem:
    name: str
    _contents: dict

    def correctlySet(self) -> bool:
        """
        Returns, if all values of the contents dict are set correctly.
        :return:
        """
        return None not in self._contents.values()
