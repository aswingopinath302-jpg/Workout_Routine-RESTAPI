from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from workoutapp.models import WorkoutSession
from workoutapp.serializers import RegisterSerializer,WorkoutSessionSerializer
from rest_framework.authentication import TokenAuthentication

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
            
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=200)

        return Response({"error": "Invalid username or password"}, status=401)

class WorkoutSessionView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        workouts = WorkoutSession.objects.filter(user=request.user)
        serializer = WorkoutSessionSerializer(workouts, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = WorkoutSessionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
            
        return Response(serializer.errors, status=400)


class WorkoutSessionDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        workout = WorkoutSession.objects.filter(id=pk, user=request.user).first()
        if workout is None:
            return Response({"error": "Workout not found"}, status=404)
            
        serializer = WorkoutSessionSerializer(workout)
        return Response(serializer.data, status=200)

    def put(self, request, pk):
        workout = WorkoutSession.objects.filter(id=pk, user=request.user).first()
        if workout is None:
            return Response({"error": "Workout not found"}, status=404)

        serializer = WorkoutSessionSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
            
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        workout = WorkoutSession.objects.filter(id=pk, user=request.user).first()
        if workout is None:
            return Response({"error": "Workout not found"}, status=404)

        workout.delete()
        return Response({"message": "Workout deleted"}, status=200)