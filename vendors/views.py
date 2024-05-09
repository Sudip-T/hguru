from .serializers import *
from .models import Category
from rest_framework.views import APIView
from rest_framework import status, filters
from rest_framework.response import Response
from core.pagination import CustomPagination
from core.permissions import IsObjectOwner
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from django.contrib.gis.geos import GEOSGeometry
from rest_framework.exceptions import MethodNotAllowed


# todo : ObjectOwner permission


class CategoryView(ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['category_name']

    # def get_permissions(self):
    #     permission_classes = [IsAuthenticated] if self.request.method \
    #         in SAFE_METHODS else [IsAuthenticated, IsAdminUser]

    #     return [permission() for permission in permission_classes]
    

class ServiceTypeView(ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    pagination_class = CustomPagination
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    search_fields = ['name']

    def get_permissions(self):
        permission_classes = [IsAuthenticated] if self.request.method in \
            SAFE_METHODS else [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]


class VendorListCreateAPIView(ListCreateAPIView):
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    search_fields = ['name']
    filterset_fields = ['category','user']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetVendorSerializer
        return VendorSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            data = request.data.copy()
            data['user'] = self.request.user.id
            serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorObjectAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.request.method)

        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return VendorSerializer
        elif self.request.method == 'GET':
            return GetVendorSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        elif self.request.user.is_authenticated:
            data = request.data.copy()
            data['user'] = self.request.user.id
            serializer = self.get_serializer(instance, data=data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VendorAddressView(ListCreateAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    queryset = VendorAddress.objects.all()
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    search_fields = ['address_line','district','province']
    filterset_fields = ['vendor']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetVendorAddressSerializer
        return VendorAddressSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorAddressObjectView(RetrieveUpdateDestroyAPIView):
    queryset = VendorAddress.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.request.method)
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return VendorAddressSerializer
        return GetVendorAddressSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        elif self.request.user.user_type == 'vendor':
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(instance, data=data, partial=partial)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorDocumentView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Documents.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomPagination
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    search_fields = ['document_type','pan_number']
    filterset_fields = ['vendor']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetVendorDocumentSerializer
        return VendorDocumentSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorDocumentObjectView(RetrieveUpdateDestroyAPIView):
    queryset = Documents.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT','DELETE']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.request.method)
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return VendorDocumentSerializer
        elif self.request.method == 'GET':
            return GetVendorDocumentSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(instance, data=data, partial=partial)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorServiceView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    pagination_class = CustomPagination
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    search_fields = ['service_name','description']
    filterset_fields = ['vendor']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetVendorServiceSerializer
        return VendorServiceSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorServiceObjectView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT','DELETE']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.request.method)
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return VendorServiceSerializer
        return GetVendorServiceSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(instance, data=data, partial=partial)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorGalleryView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Gallery.objects.all()
    pagination_class = CustomPagination
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    filterset_fields = ['vendor']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetVendorGallerySerializer
        return VendorGallerySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorGalleryObjectView(RetrieveUpdateDestroyAPIView):
    queryset = Gallery.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT','DELETE']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.request.method)
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return VendorGallerySerializer
        return GetVendorGallerySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(instance, data=data, partial=partial)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instances = self.get_object()
        print(instances)
    

class VendorFacilityView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Facility.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetVendorFacilitySerializer
        return VendorFacilitySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VendorFacilityObjectView(RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT','DELETE']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.request.method)
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return VendorFacilitySerializer
        return GetVendorFacilitySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        else:
            try:
                data = request.data.copy()
                data['vendor'] = self.request.user.vendor.id
                serializer = self.get_serializer(instance, data=data, partial=partial)
            except Exception as e:
                return Response(
                    {
                        'error':'no vendor account found'}, 
                         status=status.HTTP_403_FORBIDDEN
                    )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# class NearbyServiceProvider(APIView):
    # pagination = CustomPagination()
    #
    # def get(self,request):
    #     lat = float(request.GET.get('lat', '27.693298'))
    #     lon = float(request.GET.get('lon', '85.281653'))
    #     radius = float(request.GET.get('radius', '1000'))
    #     category = int(request.GET.get('category', '1'))
    #
    #     user_loc = GEOSGeometry(f"POINT({lon} {lat})", srid=4326)
    #
    #     # try:
    #     #     user_loc = GEOSGeometry(f"POINT({lon} {lat})", srid=4326)
    #     # except Exception as e:
    #     #     print(f"Invalid geometry: {e}")
    #
    #     nearby_vendor = Vendor.objects.filter(location__distance_lte=(user_loc, radius), category=category)
    #
    #     paginated_queryset = self.pagination.paginate_queryset(nearby_vendor, request)
    #     serializer = NearbyVendorSerializer(paginated_queryset, many=True)
    #     return self.pagination.get_paginated_response(serializer.data)
    
        # serializer = NearbyVendorSerializer(nearby_vendor, many=True).data
        # json_vendors = JsonResponse(serializer, safe=False).content.decode('utf-8')
        # context = {'vendors':json_vendors, 'radius': radius, 'user_latitude':lat, 'user_longitude':lon}

        # return render (request, 'maps.html', context)
 