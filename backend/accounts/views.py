from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh_token')

            # Blacklist the refresh token to prevent it from being used again
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"detail": "Error logging out. Please try again."}, status=400)


class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.auth.delete()  # Delete the token
        return Response({"detail": "Successfully logged out"}, status=204)
