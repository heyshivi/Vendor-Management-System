from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Avg, F
from .services import PerformanceMetricsService
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from .signals import purchase_order_acknowledged


#Vendor Details
class VendorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            vendor = self.get_object(pk)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        else:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response({"msg":"Vendor data are", "data":serializer.data})

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg" : "Vendor data are saved successfully!", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Vendor data updated successfully!", "data":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response({"msg":"Vendor data deleted Successfully!"}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)


# Purchase Order Details
class PurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            purchase_order = self.get_object(pk)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response({"msg":"Purchase Order data of this Id are", "data":serializer.data})

        else:
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response({"msg":"Purchase Order data are", "data":serializer.data})


    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg" : "Purchase Order data are saved successfully!", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Purchase Order data updated successfully!", "data":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase_order = self.get_object(pk)
        purchase_order.delete()
        return Response({"msg":"Purchase Order data deleted Successfully!"}, status=status.HTTP_204_NO_CONTENT)


    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Response({"detail": "Purchase Order not found."}, status=status.HTTP_404_NOT_FOUND)


#Performance metrics
class VendorPerformanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            metrics = PerformanceMetricsService.calculate_performance_metrics(vendor)
            return Response({"msg":"The performance metrics are", "metrics":metrics}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
        
 
 #Updating Performance metrics       
class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Trigger the signal
            purchase_order_acknowledged.send(sender=self.__class__, purchase_order=purchase_order)

            serializer = PurchaseOrderSerializer(purchase_order)
            return Response({"msg":"Performance metrics data updated successfully!", "data":serializer.data}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"detail": "Purchase Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Message": str(e), "data": None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)