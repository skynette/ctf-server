# api/views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import LeaderboardUser, Flag
from .serializers import LeaderboardUserSerializer

class SubmitFlagView(generics.CreateAPIView):
    queryset = LeaderboardUser.objects.all()
    serializer_class = LeaderboardUserSerializer

    def create(self, request, *args, **kwargs):
        # Define the dictionary of flags and their corresponding points
        flag_points = {
            'easy_flag_value': 10,
            'medium_flag_value': 20,
            'hard_flag_value': 30,
            'very_easy_flag_value': 5,
            'medium_hard_flag_value': 25,
            'super_hard_flag_value': 40,
            'another_easy_flag_value': 15,
            'tricky_flag_value': 35,
            'complex_flag_value': 50,
            'another_hard_flag_value': 30,
            'ultra_hard_flag_value': 45,
            'hidden_flag_value': 10,
            'top_secret_flag_value': 20,
            'secret_code_flag_value': 25,
            'encrypted_flag_value': 30,
            'encrypted_message_flag_value': 40,
        }

        # Get the submitted flag and username from the request data
        submitted_flag = request.data.get('flag', None)
        username = request.data.get('username', None)

        if submitted_flag and username:
            # Get or create the user based on the provided username
            user, created = LeaderboardUser.objects.get_or_create(username=username)

            # Check if the flag has already been submitted by the user
            if user.submitted_flags.filter(value=submitted_flag).exists():
                return Response({'error': 'Flag already submitted for this user'}, status=400)

            # Update the user's points based on the flag
            user.points += flag_points.get(submitted_flag, 0)

            # Create or get the Flag object for the submitted flag
            flag_obj, _ = Flag.objects.get_or_create(value=submitted_flag)
            # Add the submitted flag to the user's submitted_flags set
            user.submitted_flags.add(flag_obj)

            user.save()

            # Serialize the updated user and return the response
            serializer = LeaderboardUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Flag or username not provided'}, status=400)



class LeaderboardView(generics.ListAPIView):
    queryset = LeaderboardUser.objects.all()
    serializer_class = LeaderboardUserSerializer
