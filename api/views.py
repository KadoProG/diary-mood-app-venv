from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from .serializers import MoodcheckSerializer
from .emotion import out_parse_object


class ModelList(APIView):
    def get(self, request, format=None):
        return JsonResponse({"message": "Hello World"})


class MoodcheckModelList(APIView):

    def post(self, request, format=None):
        serializer = MoodcheckSerializer(data=request.data)
        if serializer.is_valid():
            text_value = serializer.validated_data["text"]
            result = out_parse_object(text_value)
            return JsonResponse(result)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
