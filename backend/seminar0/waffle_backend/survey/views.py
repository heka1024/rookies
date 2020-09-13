from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response

from survey.serializers import SurveyResultSerializer, OperatingSystemSerializer
from survey.models import SurveyResult, OperatingSystem

class OperatingSystemViewSet(viewsets.GenericViewSet):
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer

    # GET /api/v1/os/
    def list(self, request):
        opersatingSystems = self.get_queryset()
        return Response(self.get_serializer(opersatingSystems, many=True).data)

    # GET /api/v1/os/{os_id}/
    def retrieve(self, request, pk=None):
        # v1 : using try ~ except
        # try:
        os = self.get_object()
        return Response(self.get_serializer(os).data)
        # except ObjectDoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

class SurveyResultViewSet(viewsets.GenericViewSet):
    queryset = SurveyResult.objects.all()
    serializer_class = SurveyResultSerializer

    # GET /api/v1/survey/
    def list(self, request):
        surveys = self.get_queryset()
        return Response(self.get_serializer(surveys, many=True).data)

    # GET /api/v1/survey/{surveyresult_id}/
    def retrieve(self, request, pk=None):
        survey = get_object_or_404(SurveyResult, pk=pk)
        return Response(self.get_serializer(survey).data)
