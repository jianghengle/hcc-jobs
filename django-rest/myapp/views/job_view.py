from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.squeue import Squeue

@api_view(['GET'])
def get_squeue(request):
	user = check_session(request)
    squeue = Squeue(user.username)
    return Response(squeue.json())
