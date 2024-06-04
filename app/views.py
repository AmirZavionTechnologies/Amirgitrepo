from rest_framework import viewsets, status
from .models import Resident, Vehicle, Visitor, Guard, User
from .serializers import ResidentSerializer, VehicleSerializer, VisitorSerializer, GuardSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import csv
from django.utils.dateparse import parse_datetime


class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    

class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    
    
class VisitorViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    
class GuardViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Guard.objects.all()
    serializer_class = GuardSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ResidentSearchView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('query', '')
        residents = Resident.objects.filter(apartment_number__icontains=query)
        serializer = ResidentSerializer(residents, many=True)
        return Response(serializer.data)

class VisitorSearchView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        query= request.query_params.get('query', '')
        visits = Visitor.objects.filter(visit_code__icontains=query)
        serializer = VisitorSerializer(visits, many=True)
        return Response(serializer.data)
    
class ResidentByEntryCode(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, entry_code):
        residents = Resident.objects.filter(entry_code=entry_code)
        if not residents.exists():
            return Response({"message": "No residents found for the provided apartment number."})
        
        serializer = ResidentSerializer(residents, many=True)
        return Response(serializer.data)
    
class VehicleByEntryCode(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, entry_codes):
        vehicles = Vehicle.objects.filter(entry_codes=entry_codes)
        if not vehicles.exists():
            return Response({"message": "No vehicles found for the provided vehicle number."})
        
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    
class GuardSearchResidentByEntryCode(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, entry_code):
        try:
            resident = Resident.objects.get(entry_code=entry_code)
            serializer = ResidentSerializer(resident)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return Response({'message': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)
    
class GuardSearchVehicleByEntryCode(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, entry_codes):
        try:
            vehicle = Vehicle.objects.get(entry_codes=entry_codes)
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return Response({'message': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
    

def generate_csv_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    
    # Write CSV headers
    writer.writerow(['Type', 'Name', 'Role', 'Details'])

   
    
    # Fetch residents data
    residents = Resident.objects.all()
    
    for resident in residents:
        writer.writerow(['Resident', resident.first_name, 'Resident', f'FirstName: {resident.first_name}'])
        writer.writerow(['Resident', resident.last_name, 'Resident', f'LastName: {resident.last_name}'])
        writer.writerow(['Resident', resident.email, 'Resident', f'Email: {resident.email}'])
        writer.writerow(['Resident', resident.phone_number, 'Resident', f'phonenumber: {resident.phone_number}'])
        writer.writerow(['Resident', resident.apartment_number, 'Resident', f'Apartmentnumber: {resident.apartment_number}'])
        writer.writerow(['Resident', resident.cnic_number, 'Resident', f'CNIC: {resident.cnic_number}'])
        writer.writerow(['Resident', resident.age, 'Resident', f'Age: {resident.age}'])
        writer.writerow(['Resident', resident.numberofpersons, 'Resident', f'Numberofpersons: {resident.numberofpersons}'])
        writer.writerow(['Resident', resident.entry_code, 'Resident', f'entrycode: {resident.entry_code}'])

    # Fetch visitors data
    visitors = Visitor.objects.all()
    
    for visitor in visitors:
        writer.writerow(['Visitor', visitor.first_name, 'Visitor', f'FirstName: {visitor.first_name}'])
        writer.writerow(['Visitor', visitor.last_name, 'Visitor', f'LastName: {visitor.last_name}'])
        writer.writerow(['Visitor', visitor.phone_number, 'Visitor', f'PhoneNumber: {visitor.phone_number}'])
        writer.writerow(['Visitor', visitor.vehicle_number, 'Visitor', f'VehicleNumber: {visitor.vehicle_number}'])
        writer.writerow(['Visitor', visitor.visit_date, 'Visitor', f'Date: {visitor.visit_date}'])
        writer.writerow(['Visitor', visitor.visit_code, 'Visitor', f'VisitCode: {visitor.visit_code}'])

    
    
    
    return response