# api/views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import LeaderboardUser, Flag
from .serializers import LeaderboardUserSerializer
from django.utils.text import slugify

class SubmitFlagView(generics.CreateAPIView):
    queryset = LeaderboardUser.objects.all()
    serializer_class = LeaderboardUserSerializer

    def create(self, request, *args, **kwargs):
        # Define the dictionary of flags and their corresponding points
        flag_points = {
            'very_easy_fl4g': 5,
            'a_very_easy_fl4g': 5,
            'hidden_fl4g': 10,
            'easy_fl4g': 10,
            'another_easy_fl4g': 15,
            'whisper_fl4g': 15,
            'top_secret_fl4g': 20,
            'medium_fl4g': 20,
            'moonlight_fl4g': 20,
            'secret_code_fl4g': 25,
            'medium_hard_fl4g': 25,
            'cipher_fl4g': 25,
            'thunderstorm_fl4g': 25,
            'hard_fl4g': 30,
            'another_hard_fl4g': 30,
            'encrypted_fl4g': 30,
            'sphinx_fl4g': 30,
            'phantom_fl4g': 30,
            'tricky_fl4g': 35,
            'shadow_fl4g': 35,
            'firestorm_fl4g': 35,
            'ninja_fl4g': 35,
            'super_hard_fl4g': 40,
            'encrypted_message_fl4g': 40,
            'mind_bender_fl4g': 40,
            'nebula_fl4g': 40,
            'jigsaw_fl4g': 40,
            'quantum_fl4g': 45,
            'ultra_hard_fl4g': 45,
            'enigma_fl4g': 45,
            'avalanche_fl4g': 45,
            'galaxy_fl4g': 50,
            'complex_fl4g': 50,
            'xXx_unbreakable_fl4g_xXx': 50
        }

        # Get the submitted flag and username from the request data
        submitted_flag = request.data.get('flag', None)
        username = request.data.get('username', None)

        if submitted_flag and username:
            submitted_flag = slugify(submitted_flag)
            if not flag_points.get(submitted_flag, None):
                return Response({'error': 'Flag not valid'}, status=400)

            # Get or create the user based on the provided username
            user, created = LeaderboardUser.objects.get_or_create(username=username)

            # Check if the flag has already been submitted by the user
            if user.submitted_flags.filter(value=submitted_flag).exists():
                return Response({'error': 'Flag already submitted for this user'}, status=400)

            # Update the user's points based on the flag
            score = flag_points.get(submitted_flag, 0)
            user.points += score

            # Create or get the Flag object for the submitted flag
            flag_obj, _ = Flag.objects.get_or_create(value=submitted_flag)
            # Add the submitted flag to the user's submitted_flags set
            user.submitted_flags.add(flag_obj)

            user.save()

            # Serialize the updated user and return the response
            serializer = LeaderboardUserSerializer(user)
            return Response({'score': score})
        else:
            return Response({'error': 'Flag or username not provided'}, status=400)



class LeaderboardView(generics.ListAPIView):
    queryset = LeaderboardUser.objects.all()
    serializer_class = LeaderboardUserSerializer
