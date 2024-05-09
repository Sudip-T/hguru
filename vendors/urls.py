from .views import *
from rest_framework import routers
from django.urls import path,include


router = routers.DefaultRouter()
router.register(r'category', CategoryView, basename='category')
router.register(r'service-type', ServiceTypeView, basename='service-type')

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendors'),
    path('vendors/<int:pk>/', VendorObjectAPIView.as_view(), name='vendor-object'),

    path('vendor-address/', VendorAddressView.as_view(), name='vendor-address'),
    path('vendor-address/<int:pk>/', VendorAddressObjectView.as_view(), name='vendor-adddress-obj'),

    path('vendor-document/', VendorDocumentView.as_view(), name='vendor-documents'),
    path('vendor-document/<int:pk>/', VendorDocumentObjectView.as_view(), name='vendor-document-obj'),

    path('vendor-service/', VendorServiceView.as_view(), name='vendor-services'),
    path('vendor-service/<int:pk>/', VendorServiceObjectView.as_view(), name='vendor-service-obj'),

    path('vendor-gallery/', VendorGalleryView.as_view(), name='vendor-galleries'),
    path('vendor-gallery/<int:pk>/', VendorGalleryObjectView.as_view(), name='vendor-gallery-obj'),

    path('vendor-facility/', VendorFacilityView.as_view(), name='vendor-facilities'),
    path('vendor-facility/<int:pk>/', VendorFacilityObjectView.as_view(), name='vendor-facility-obj'),

    # path('nearby-vendor/', NearbyServiceProvider.as_view(), name='find_service_providers'),

]