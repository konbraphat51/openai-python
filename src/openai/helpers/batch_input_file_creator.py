from collections import UserList
from pathlib import Path

from typing import Iterable, Union

from ..types import BatchRequestInputObject

class BatchInputFileCreator(UserList[BatchRequestInputObject]):
    """
    A helper class to create a batch input file for OpenAI's Batch API.
    
    Add `BatchRequestInputObject` instances to this class like a list and then call `create_file()`
    """
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
        if not custom_id_valid and raise_validation:
                raise ValueError("Custom IDs must be unique across all items in the batch input file.")

        endpoint_valid = self._validate_endpoint()
        if not endpoint_valid and raise_validation:
            raise ValueError("All items in the batch input file must have the same endpoint.")

    def _validate_custom_id(self) -> bool:
        """Check duplication of custom IDs in the batch input objects."""

        custom_ids: set[str] = set()
        for item in self:
            if item.custom_id in custom_ids:
                return False
            custom_ids.add(item.custom_id)
        return True
    
    def _validate_endpoint(self) -> bool:
        """Check if the endpoints are all the same."""
        # Placeholder for actual endpoint validation logic
        
        endpoints = {item.url for item in self}
        return len(endpoints) == 1
