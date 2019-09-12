from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.my_job import Squeue, JobDetail
from . import check_session


@api_view(['GET'])
def get_squeue(request):
    user = check_session(request)
    squeue = Squeue(user.username)
    return Response(squeue.json())


@api_view(['GET'])
def get_job_detail(request, job_id):
    user = check_session(request)
    job = JobDetail(user.username, job_id)
    return Response(job.json())
