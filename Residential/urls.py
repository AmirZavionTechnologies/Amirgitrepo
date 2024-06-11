from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, GuardsSearchResidentByEntryCode,GuardSearchResidentByApartmentView ,ResidentsByEntryCode, VehicleViewSet, GuardsSearchVehicleByEntryCode, VehiclesByEntryCode, GuardViewSet, RegisterResidentView, RegisterGuardView, LoginView, resident_list,  guard_list
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView



router = DefaultRouter()
router.register(r'residentsnew', ResidentViewSet)
router.register(r'vehicleset', VehicleViewSet)
router.register(r'Guardset', GuardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('guards/search-residents/<str:entry_code>/', GuardsSearchResidentByEntryCode.as_view(), name='guard-search-resident'),
    path('searchresident/<str:entry_code>/', ResidentsByEntryCode.as_view(), name='resident-by-apartment-number'),
    path('searchvehicle/<str:entry_codes>/', VehiclesByEntryCode.as_view(), name='vehicle-by-vehicle-number'),
    path('guards/search/<str:apartment_number>/', GuardSearchResidentByApartmentView.as_view(), name='guard-search-resident'),
    path('guards/search-vehicles/<str:entry_codes>/',GuardsSearchVehicleByEntryCode.as_view(),name='guard-search-vehicle'),
    path('register/resident/', RegisterResidentView.as_view(), name='register-resident'),
    path('api/register/guard/', RegisterGuardView.as_view(), name='register-guard'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/residents/', resident_list, name='resident-list'),
    path('api/guards/', guard_list, name='guard-list'),
]