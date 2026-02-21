from datetime import timedelta
from datetime import date
import pytest
from models.stocking import Batch
from models.stocking import OrderLine
from service.stock_allocator.abstract_stock_allocator import IStockAllocator
from service.stock_allocator.exceptions import OutOfStock
from service.stock_allocator.stock_allocator import StockAllocator


@pytest.fixture
def stock_allocator() -> StockAllocator:
    return StockAllocator()


def test_can_allocate_if_available_greater_than_required(stock_allocator: IStockAllocator):
    batch = Batch(reference="batch-001", sku="SMALL-TABLE", quantity=20)
    orderline = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=3)

    assert stock_allocator.can_allocate(batch, orderline) is True


def test_cannot_allocate_if_available_smaller_than_required(stock_allocator: IStockAllocator):

    batch = Batch(reference="batch-001", sku="SMALL-TABLE", quantity=2)
    orderline = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=3)

    assert stock_allocator.can_allocate(batch, orderline) is False


def test_cannot_allocate_if_sku_does_not_match(stock_allocator: IStockAllocator):

    batch = Batch(reference="batch-001", sku="LARGE-TABLE", quantity=20)
    orderline = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=3)

    assert stock_allocator.can_allocate(batch, orderline) is False


def test_can_only_deallocate_allocated_lines(stock_allocator: IStockAllocator):
    batch = Batch(reference="batch-001", sku="SMALL-TABLE", quantity=20)
    orderline = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=3)

    stock_allocator.deallocate(batch, orderline)

    assert stock_allocator.get_available_quantity(batch) == 20


def test_allocation_is_idempotent(stock_allocator: IStockAllocator):
    batch = Batch(reference="batch-001", sku="SMALL-TABLE", quantity=20)
    orderline = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=3)

    stock_allocator.allocate(batch, orderline)
    stock_allocator.allocate(batch, orderline)

    assert stock_allocator.get_available_quantity(batch) == 17


def test_preferes_current_stock_over_shipments(stock_allocator: IStockAllocator):
    target_batch = Batch(reference="batch-001", sku="SMALL-TABLE", quantity=20)
    batches = [
        Batch(reference="batch-002", sku="SMALL-TABLE", quantity=2),
        Batch(reference="batch-003", sku="SMALL-TABLE", quantity=20, eta=date.today() + timedelta(days=1)),
        Batch(reference="batch-004", sku="SMALL-TABLE", quantity=20, eta=date.today() + timedelta(days=2)),
        target_batch, ]

    orderline = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=3)

    allocated_batch = stock_allocator.allocate_multiple(orderline, batches)

    assert allocated_batch == target_batch.reference


def test_raises_out_of_stock_if_cannot_allocate(stock_allocator: IStockAllocator):
    batches = [
        Batch(reference="batch-001", sku="SMALL-TABLE", quantity=2),
        Batch(reference="batch-002", sku="SMALL-TABLE", quantity=3), ]
    orderline = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=4)

    with pytest.raises(OutOfStock):
        stock_allocator.allocate_multiple(orderline, batches)
