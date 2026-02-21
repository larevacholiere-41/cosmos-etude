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
        Returns True if the batch can allocate the order line, False otherwise.
        '''
        ...

    def allocate(self, batch: Batch, orderline: OrderLine) -> Batch:
        '''
        Allocates the order line to the batch.
        Returns the updated batch.
        '''
        ...

    def deallocate(self, batch: Batch, orderline: OrderLine) -> Batch:
        '''
        Deallocates the order line from the batch.
        Returns the updated batch.
        '''
        ...

    def get_available_quantity(self, batch: Batch) -> int:
        '''
        Returns the quantity of the batch that is available to allocate.
        '''
        ...
