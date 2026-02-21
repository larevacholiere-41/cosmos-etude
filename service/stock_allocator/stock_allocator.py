from models.stocking import Batch
from models.stocking import OrderLine


class StockAllocator:
    '''
    Interface for a stock allocator.
    A stock allocator is responsible for allocating stock to order lines.
    It should keep track of the allocated stock and the remaining stock for processed batches.
    '''

    def __init__(self):
        self.allocations: set[tuple[Batch, OrderLine]] = set()

    def can_allocate(self, batch: Batch, orderline: OrderLine) -> bool:
        '''
        Returns True if the batch can allocate the order line, False otherwise.
        '''
        return all([batch.quantity >= orderline.quantity, batch.sku == orderline.sku])

    def allocate(self, batch: Batch, orderline: OrderLine) -> None:
        '''
        Allocates the order line to the batch.
        '''
        if self.can_allocate(batch, orderline):
            self.allocations.add((batch, orderline))

    def deallocate(self, batch: Batch, orderline: OrderLine) -> None:
        '''
        Deallocates the order line from the batch.
        '''
        if (batch, orderline) in self.allocations:
            self.allocations.remove((batch, orderline))

    def get_available_quantity(self, batch: Batch) -> int:
        '''
        Returns the quantity of the batch that is available to allocate.
        '''
        return batch.quantity - sum(orderline.quantity for batch, orderline in self.allocations)
