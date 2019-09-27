from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.jupyter import Jupyter
from . import check_session


@api_view(['GET'])
def get_jupyters(request, cluster):
    user = check_session(request)
    jupyters = Jupyter.get_by_user(cluster, user)
    return Response([j.json() for j in jupyters])


@api_view(['POST'])
def start_jupyter(request):
    user = check_session(request)
    cluster = request.data['cluster']
    jupyter = Jupyter.create(cluster, user)
    return Response(jupyter.json())


@api_view(['POST'])
def stop_jupyter(request):
    user = check_session(request)
    jupyter_id = request.data['jupyterId']
    Jupyter.stop(user, jupyter_id)
    return Response({'ok': True})
