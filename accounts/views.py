from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from accounts.emails import send_otp_via_email
from .serializer import *




# Create your views here.
class VerifyOTP(APIView):
        def post(self, request):
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                    'status' : 400,
                    'message' : 'something went wrong.',
                    'data' : 'invalid email'
                })
                if user[0].otp != otp:
                    return Response({
                    'status' : 400,
                    'message' : 'something went wrong.',
                    'data' : 'wrong otp'
                })
                user[0].is_verified = True
                user[0].save()

                return Response({
                    'status': 200,
                    'message' : 'account verified.',
                    'data' : serializer.data,
                })



class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_otp_via_email(serializer.data['email'])
            return Response({
                'status': 200,
                'message' : 'registration succesfully check your email.',
                'data' : serializer.data,
            })

        return Response({
            'status' : 400,
            'message' : 'something went wrong.',
            'data' : serializer.errors
        })
        


        # try:
        #     serializer = UserSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         send_otp_via_email(serializer.data['email'])
        #         return Response({
        #             'status': 200,
        #             'message' : 'registration succesfully check your email.',
        #             'data' : serializer.data,
        #         })


        #     return Response({
        #         'status' : 400,
        #         'message' : 'something went wrong.',
        #         'data' : serializer.errors
        #     })

        # except Exception as e:
        #     print(e)

    