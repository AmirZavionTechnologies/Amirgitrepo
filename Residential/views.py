from rest_framework import viewsets, status
from .models import Residentsdata, Vehiclesdata, User, Guard
from .serializers import ResidentSerializer, VehicleSerializer, UserSerializer, GuardSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.authtoken.models import Token


class RegisterResidentView(generics.CreateAPIView):
    queryset = Residentsdata.objects.all()
    serializer_class = ResidentSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = Residentsdata.objects.get(user__username=response.data['user']['username'])
        token, created = Token.objects.get_or_create(user=user.user)
        response.data['token'] = token.key
        return response


class RegisterGuardView(generics.CreateAPIView):
    serializer_class = GuardSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resident_list(request):
    residents = Residentsdata.objects.all()
    serializer = ResidentSerializer(residents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def guard_list(request):
    guards = Guard.objects.all()
    serializer = GuardSerializer(guards, many=True)
    return Response(serializer.data)



# Create your views here.
class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Residentsdata.objects.all()
    serializer_class = ResidentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resident = serializer.save()

        # Set the current user as the resident
        resident.user = request.user
        resident.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # Return an empty queryset to prevent listing
        return Residentsdata.objects.none()
    
class VehicleViewSet(viewsets.ModelViewSet):
    queryset=Vehiclesdata.objects.all()
    serializer_class=VehicleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()

        # Set the current user as the resident
        vehicle.user = request.user
        vehicle.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # Return an empty queryset to prevent listing
        return Vehiclesdata.objects.none()

class GuardSearchResidentByApartmentView(APIView):
    def get(self, request, apartment_number):
        try:
            residents = Residentsdata.objects.filter(apartment_number=apartment_number)
            serializer = ResidentSerializer(residents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Residentsdata.DoesNotExist:
            return Response(data={'message': 'Residents not found for the provided apartment number'}, status=status.HTTP_404_NOT_FOUND)
    

class GuardsSearchVehicleByEntryCode(APIView):
    
    
    def get(self, request, entry_codes):
        try:
            vehicle = Vehiclesdata.objects.get(entry_codes=entry_codes)
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehiclesdata.DoesNotExist:
            return Response({'message': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)



class GuardsSearchResidentByEntryCode(APIView):
    

    def get(self, request, entry_code):
        try:
            resident = Residentsdata.objects.get(entry_code=entry_code)
            serializer = ResidentSerializer(resident)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Residentsdata.DoesNotExist:
            return Response({'message': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)

class ResidentsByEntryCode(APIView):

    def get(self, request, entry_code):
        residents = Residentsdata.objects.filter(entry_code=entry_code)
        if not residents.exists():
            return Response({"message": "No residents found for the provided apartment number."})
        
        serializer = ResidentSerializer(residents, many=True)
        return Response(serializer.data)  

class VehiclesByEntryCode(APIView):

    def get(self, request, entry_codes):
        vehicles=Vehiclesdata.objects.filter(entry_codes=entry_codes)
        if not vehicles.exists():
             return Response({"message": "No vehicles found for the provided apartment number."})
        
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)  
    
class UserSerializer(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GuardViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Guard.objects.all()
    serializer_class = GuardSerializer