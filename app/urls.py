from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, VehicleViewSet, VisitorViewSet, GuardViewSet, UserViewSet, ResidentSearchView, VisitorSearchView, ResidentByEntryCode, VehicleByEntryCode, GuardSearchResidentByEntryCode,GuardSearchVehicleByEntryCode ,generate_csv_report


router = DefaultRouter()
router.register(r'residents', ResidentViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'visitors', VisitorViewSet)
router.register(r'guards',GuardViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('guards/search/residents/', ResidentSearchView.as_view(), name='guard-search-residents'),
    path('guards/search/visitors/',VisitorSearchView.as_view(),name='guard-search-visitor'),
    path('resident/<str:entry_code>/', ResidentByEntryCode.as_view(), name='resident-by-apartment-number'),
    path('vehicle/<str:entry_codes>/', VehicleByEntryCode.as_view(), name='vehicle-by-number'),
    path('guards/search-resident/<str:entry_code>/', GuardSearchResidentByEntryCode.as_view(), name='guard-search-resident'),
    path('guards/search-vehicle/<str:entry_codes>/', GuardSearchVehicleByEntryCode.as_view(), name='guard-search-resident'),
    path('generate-csv-report/', generate_csv_report , name='generate_csv_report'),
]