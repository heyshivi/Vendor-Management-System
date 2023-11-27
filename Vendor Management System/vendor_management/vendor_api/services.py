from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta


class PerformanceMetricsService:
    @staticmethod
    def calculate_performance_metrics(vendor):
        completed_pos = vendor.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        print(total_completed_pos)

        # On-Time Delivery Rate
        on_time_delivery_rate = completed_pos.filter(delivery_date__lte=timezone.now()).count() / total_completed_pos if total_completed_pos != 0 else 0

        # Quality Rating Average
        quality_rating_avg = completed_pos.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

        # Average Response Time
        
        response_times = [(po.acknowledgment_date - po.issue_date) for po in completed_pos]
        avg_response_time = sum(response_times, timedelta()) / len(response_times) if response_times else timedelta(0)

        # Fulfilment Rate
        fulfillment_rate = completed_pos.filter(quality_rating__isnull=True).count() / total_completed_pos if total_completed_pos != 0 else 0

        return {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': avg_response_time.total_seconds() if avg_response_time else 0,
            'fulfillment_rate': fulfillment_rate,
        }
