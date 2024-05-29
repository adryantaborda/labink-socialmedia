from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import rest_framework.status as status
from authapp.models import User
from .serializers import UserSerializer, UserLoginSerializer, UserRegisterSerializer, UserDeleteAccountSerializer
from django.http import JsonResponse
from rest_framework import authentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated



@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/users',
        'GET /api/users/:id',
        'POST api/login/',
        'POST /api/register',
        'POST /api/delete/',
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPK(request,pk,format=None):
    try:
        user = User.objects.get(id=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['POST'])
def postUser(request):
    if request.method == 'POST':
        data = request.data
        
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"ERROR":"User already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Created User:", serializer.data["username"]},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def loginUser(request):
    data = request.data
    serializer = UserLoginSerializer(data=data)

    if serializer.is_valid():
        
        serializer.perform_login()
        return Response({"Success:", "User logged succesfully"},status=status.HTTP_200_OK)
    else:
        print(serializer.is_valid())
        return Response({"ERROR":"NO PERMISSION."}, status=status.HTTP_400_BAD_REQUEST)


# PANI NO SISTEMA UIIIIIIIIIIIIIIIIIIIIIIIUUUUUUUUUUUU
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteUser(request,format=None):
    user = request.user
    data = request.data
    print(user)
    print(data)

    serializer = UserDeleteAccountSerializer(data=data)
    if serializer.is_valid():
            if user.username == request.validated_data['username']:
                serializer.perform_delete()
                return Response({"Success:", "User deleted succesfully"},status=status.HTTP_200_OK)
            else:
                return Response({"ERROR":"NO PERMISSION."}, status=status.HTTP_400_BAD_REQUEST)
            
    
    print("WRONG SERIALIZER") 
    print(serializer.is_valid())       
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
