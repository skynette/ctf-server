# api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LeaderboardUser, Flag, Config
from .serializers import LeaderboardUserSerializer
from django.utils.text import slugify
from django.utils import timezone

class SubmitFlagView(generics.CreateAPIView):
    queryset = LeaderboardUser.objects.all()
    serializer_class = LeaderboardUserSerializer

    def create(self, request, *args, **kwargs):
        # Check if game has started
        config = Config.get_config()
        if not config.game_started:
            return Response({'error': 'Game has not started yet'}, status=403)
        
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
            'xXx_unbreakable_fl4g_xXx': 80
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
            
            # Get the count of other users who submitted the same flag
            flag = Flag.objects.filter(value=submitted_flag).first()
            if flag:
                other_users_count = LeaderboardUser.objects.filter(submitted_flags=flag).count()
            else: other_users_count = 0
            # Calculate the multiplier based on the number of other users
            multiplier = 1 + other_users_count

            # Check if the flag has already been submitted by the user
            if user.submitted_flags.filter(value=submitted_flag).exists():
                return Response({'error': 'Flag already submitted for this user'}, status=400)
            
             # Reduce the score by the calculated multiplier
            score = flag_points[submitted_flag] // multiplier
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


class GameControlView(APIView):

    def post(self, request):
        """
        Start or end the game based on the action parameter.
        Expects: {"action": "start"} or {"action": "end"}
        """
        action = request.data.get('action', None)
        password = request.data.get('password', None)
        config = Config.get_config()
        print("config", config)
        print("action and password", action, password)

        if action == 'start' and password == config.password:
            if config.game_started:
                return Response({
                    'error': 'Game has already started'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            config.game_started = True
            config.start_time = timezone.now()
            config.end_time = None
            config.save()
            
            return Response({
                'message': 'Game started successfully',
                'start_time': config.start_time
            })

        elif action == 'end' and password == config.password:
            if not config.game_started:
                return Response({
                    'error': 'Game has not been started yet'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            config.game_started = False
            config.end_time = timezone.now()
            config.save()
            
            return Response({
                'message': 'Game ended successfully',
                'end_time': config.end_time,
                'duration': config.end_time - config.start_time
            })

        return Response({
            'error': 'Invalid action or password. Use "start" or "end".'
        }, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        """Return the current game state"""
        config = Config.get_config()
        return Response({
            'game_started': config.game_started,
            'start_time': config.start_time,
            'end_time': config.end_time,
            'duration': config.end_time - config.start_time if (config.end_time and config.start_time) else None
        })