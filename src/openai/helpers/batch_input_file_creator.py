from collections import UserList
from pathlib import Path

from typing import Iterable, Union

from ..types import BatchRequestInputObject

class BatchInputFileCreator(UserList[BatchRequestInputObject]):
    def __init__(
            self,
            initlist: Union[Iterable[BatchRequestInputObject], None] = None,
    ) -> None:
        super().__init__(initlist or [])

    def create_file(
        self,
        file_path: Union[Path, str],
        raise_validation: bool = True,    
    ) -> None:
        """Create a batch input file available for Batch API"""
        self.validate(raise_validation)
        
        # handle file path
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # save file
        with file_path.open("w") as f:
            f.write(self.get_plain_text())

    def get_plain_text(self) -> str:
        """Get the plain text representation of the batch input file."""
        return "\n".join(item.to_json() for item in self)

    def validate(self, raise_validation: bool) -> None:
        """ Validate the batch input file for uniqueness of custom IDs."""
        
        custom_id_valid = self._validate_custom_id()
        if not custom_id_valid:
            if raise_validation:
                raise ValueError("Custom IDs must be unique across all items in the batch input file.")

    def _validate_custom_id(self) -> bool:
        """Check duplication of custom IDs in the batch input objects."""

        custom_ids: set[str] = set()
        for item in self:
            if item.custom_id in custom_ids:
                return False
            custom_ids.add(item.custom_id)
        return True