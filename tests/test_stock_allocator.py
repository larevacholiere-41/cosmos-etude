import pytest
from models.stocking import Batch
from models.stocking import OrderLine
from service.stock_allocator.abstract_stock_allocator import IStockAllocator
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
