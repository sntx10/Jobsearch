from django.contrib.auth import get_user_model
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accountify.serializers import RegisterSerializer, ChangePasswordSerializer, DeleteAccountSerializer

# Create your views here.

User = get_user_model()


class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            'You have successfully registered.'
            'An activation email has been sent to you',
            status=status.HTTP_201_CREATED
        )


class ActivationAPIView(APIView):
    def get(self, request, activation_code, is_mentor=False):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ""
            user.save()
            return Response(
                {"Message": "Successfully activated."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"Message": "Wrong email."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response('Password changed successfully', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=DeleteAccountSerializer)
    def post(self, request):
        password = request.data.get('password')
        if not request.user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)