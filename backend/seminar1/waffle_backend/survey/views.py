from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from survey.serializers import OperatingSystemSerializer, SurveyResultSerializer
from survey.models import OperatingSystem, SurveyResult

def check_num(x):
    if not x.isdigit():
        return False
    n = int(x)
    if n >= 1 or n <= 5:
        return True
    return False

class SurveyResultViewSet(viewsets.GenericViewSet):
    queryset = SurveyResult.objects.all()
    serializer_class = SurveyResultSerializer

    # GET /api/v1/survey/
    def list(self, request):
        surveys = self.get_queryset().select_related('os')
        return Response(self.get_serializer(surveys, many=True).data)

    # POST /api/v1/survey
    def create(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        python = request.data.get('python')
        rdb = request.data.get('rdb')
        programming = request.data.get('programming')
        os_name = request.data.get('os')

        xs = (python, rdb, programming)

        if any(not x for x in xs):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if any(not check_num(x) for x in xs):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        os, _ = OperatingSystem.objects.get_or_create(name=os_name)

        data = [int(x) for x in xs]

        survey = SurveyResult.objects.create(
            os=os, 
            python=data[0], 
            rdb=data[1],
            programming=data[2],
            user_id = user
        )

        return Response(self.get_serializer(survey).data)


    # GET /api/v1/survey/{id}
    def retrieve(self, request, pk=None):
        survey = get_object_or_404(SurveyResult, pk=pk)
        return Response(self.get_serializer(survey).data)


class OperatingSystemViewSet(viewsets.GenericViewSet):
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer

    # GET /api/v1/os/
    def list(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    # GET /api/v1/os/{id}/
    def retrieve(self, request, pk=None):
        try:
            os = OperatingSystem.objects.get(id=pk)
        except OperatingSystem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(os).data)
