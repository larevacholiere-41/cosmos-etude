from models.stocking import Batch
from models.stocking import OrderLine
from service.stock_allocator.exceptions import OutOfStock


class StockAllocator:
    '''
    Concrete stock allocator implementation.

    Allocates stock to order lines and keeps track of
    allocated stock and remaining stock for processed batches.
    '''

    def __init__(self):
        self.allocations: set[tuple[Batch, OrderLine]] = set()

    def can_allocate(self, batch: Batch, orderline: OrderLine) -> bool:
        '''
        Check whether the batch can fulfill the order line.

        Args:
            batch: The batch to check availability against.
            orderline: The order line requesting allocation.

        Returns:
            True if the batch can allocate the order line, False otherwise.
        '''
        return all([batch.quantity >= orderline.quantity, batch.sku == orderline.sku])

    def allocate(self, batch: Batch, orderline: OrderLine) -> None:
        '''
        Allocate the order line to the batch.

        Args:
            batch: The batch to allocate against.
            orderline: The order line to allocate.
        '''
        if self.can_allocate(batch, orderline):
            self.allocations.add((batch, orderline))

    def deallocate(self, batch: Batch, orderline: OrderLine) -> None:
        '''
        Deallocate the order line from the batch.

        Args:
            batch: The batch to deallocate from.
            orderline: The order line to remove.
        '''
        if (batch, orderline) in self.allocations:
            self.allocations.remove((batch, orderline))

    def get_available_quantity(self, batch: Batch) -> int:
        '''
        Get the quantity of the batch that is available to allocate.

        Args:
            batch: The batch to check.

        Returns:
            The available quantity remaining in the batch.
        '''
        return batch.quantity - sum(orderline.quantity for batch, orderline in self.allocations)

    def _sort_batches_by_eta(self, batches: list[Batch]) -> list[Batch]:
        '''
        Sort the batches by ETA, with None (in-warehouse) first.

        Uses an explicit sorting function rather than ``__gt__`` because ETA
        is not the only natural ordering for batches (quantity, reference, etc.).

        Args:
            batches: The batches to sort.

        Returns:
            A new list of batches sorted by ETA in ascending order.
        '''
        # None first (i.e. lowest), then sort by ETA
        return sorted(batches, key=lambda x: (x.eta is not None, x.eta))

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

        for batch in self._sort_batches_by_eta(batches):
            if self.can_allocate(batch, orderline):
                self.allocate(batch, orderline)
                return batch.reference

        raise OutOfStock
