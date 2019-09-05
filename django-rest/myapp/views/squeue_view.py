from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.squeue import Squeue

@api_view(['POST'])
def request_squeue(request):
    username = request.data['username']
    squeue = Squeue(username)
    return Response(squeue.json())