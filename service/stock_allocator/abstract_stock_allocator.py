from typing import Protocol

from models.stocking import Batch
from models.stocking import OrderLine


class IStockAllocator(Protocol):
    '''
    Interface for a stock allocator.
    A stock allocator is responsible for allocating stock to order lines.
    It should keep track of the allocated stock and the remaining stock for processed batches.
    '''

    def can_allocate(self, batch: Batch, orderline: OrderLine) -> bool:
        '''
        Check whether the batch can fulfill the order line.

        Args:
            batch: The batch to check availability against.
            orderline: The order line requesting allocation.

        Returns:
            True if the batch can allocate the order line, False otherwise.
        '''
        ...

    def allocate(self, batch: Batch, orderline: OrderLine) -> None:
        '''
        Allocate the order line to the batch.

        Args:
            batch: The batch to allocate against.
            orderline: The order line to allocate.
        '''
        ...

    def allocate_multiple(self, orderline: OrderLine, batches: list[Batch]) -> str:
        '''
        Allocate the order line to the most relevant batch from the list.

        A batch can be allocated to multiple order lines,
        but one line can only be allocated to one batch.

        Args:
            orderline: The order line to allocate.
            batches: The list of candidate batches to allocate from.

        Returns:
            The reference of the batch that was allocated to the order line.

        Raises:
            OutOfStock: If the order line cannot be allocated to any batch.
        '''
        ...

    def deallocate(self, batch: Batch, orderline: OrderLine) -> Batch:
        '''
        Deallocate the order line from the batch.

        Args:
            batch: The batch to deallocate from.
            orderline: The order line to remove.

        Returns:
            The updated batch after deallocation.
        '''
        ...

    def get_available_quantity(self, batch: Batch) -> int:
        '''
        Get the quantity of the batch that is available to allocate.

        Args:
            batch: The batch to check.

        Returns:
            The available quantity remaining in the batch.
        '''
        ...
