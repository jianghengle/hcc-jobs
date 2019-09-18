from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.my_job import Jobs, JobDetail, Job
from . import check_session


@api_view(['GET'])
def get_jobs(request, start_date):
    user = check_session(request)
    jobs = Jobs(user, start_date)
    return Response(jobs.json())


@api_view(['GET'])
def get_job_detail(request, job_id):
    user = check_session(request)
    job = JobDetail(user, job_id)
    return Response(job.json())


@api_view(['POST'])
def cancel_job(request):
    user = check_session(request)
    job_id = request.data['jobId']
    job = Job(user, job_id)
    job.cancel_job()
    return Response({'ok': True})
