from customers.models import Customer 
from django.http import JsonResponse, Http404
from customers.serializer import CustomerSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes #which methods are allowed
from rest_framework.response import Response # let us handle response
from rest_framework import status #give us options for status code
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def customers(request):
        #invoke serializer and return to customer 
        if request.method == 'GET':
                data = Customer.objects.all()
                serializer = CustomerSerializer(data,many=True)
                return Response({'customer':serializer.data}, status = status.HTTP_200_OK)
        elif request.method == 'POST':
                serializer = CustomerSerializer(data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response({'customer':serializer.data},status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET','POST','DELETE']) #this describe the functionality for this fuction 
@permission_classes([IsAuthenticated])
def customer(request,id):
        try:
                data = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
                #raise Http404("Customer not exist")
                return Response(status = status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
                serializer = CustomerSerializer(data)
                return Response({'customer':serializer.data}, status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
                data.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'POST':
                serializer = CustomerSerializer(data, data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response({'customer':serializer.data})
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                tokens = {
                        'refresh' : str(refresh),
                        'access' : str(refresh.access_token)
                }
                return Response(tokens,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
