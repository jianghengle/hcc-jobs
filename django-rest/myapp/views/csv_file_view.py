from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.csv_file import CsvFile

@api_view(['Get'])
def get_csv(request, filename):
    csv = CsvFile(filename)
    return Response(csv.json())