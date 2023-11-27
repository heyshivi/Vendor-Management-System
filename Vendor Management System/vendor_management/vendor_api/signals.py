from django.db.models.signals import Signal
from django.dispatch import receiver
from .services import PerformanceMetricsService

purchase_order_acknowledged = Signal()

@receiver(purchase_order_acknowledged)
def handle_purchase_order_acknowledged(sender, purchase_order, **kwargs):
    print("Performance Metrics is updated")
    vendor = purchase_order.vendor
    PerformanceMetricsService.calculate_performance_metrics(vendor)
