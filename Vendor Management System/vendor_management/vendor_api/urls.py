
from django.urls import path
from .views import VendorView, PurchaseOrderView, VendorPerformanceView, AcknowledgePurchaseOrderView

urlpatterns = [
    path('vendors/', VendorView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorView.as_view(), name='vendor-detail'),
    path('purchase_orders/', PurchaseOrderView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderView.as_view(), name='purchase-order-detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
]

