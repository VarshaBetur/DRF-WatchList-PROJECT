from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models  #comment for jwt authentication
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def registration_view(request):
    if request.method=='POST':
        serializer=RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()

            data["response"]="Registration Successful!"
            data["username"]=account.username
            data["email"]=account.email

            token=Token.objects.get(user=account).key
            data["token"] = token    #token authentication


            # refresh = RefreshToken.for_user(account)  #jwt authentication
            # data["token"] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }

        else:
            data=serializer.errors
        return Response(data,status=status.HTTP_201_CREATED)