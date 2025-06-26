from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import reverse, status
from django.shortcuts import get_object_or_404, redirect

from .models import ShortenedURL
from .serializers import ShortenedURLSerializer

class ShortenURLView(APIView):
    def post(self, request):
        serializer = ShortenedURLSerializer(data=request.data)
        if serializer.is_valid():
            instance = ShortenedURL.objects.create(**serializer.validated_data)
            instance.save()

            relative_url = reverse('redirect', args=[instance.shortened_url])
            full_url = request.build_absolute_uri(relative_url)

            return Response({"shortened_url": full_url}, status=201)
        return Response(serializer.errors, status=400)

class OriginalURLView(APIView):
    def get(self, request, shortened_url):
        try:
            url = ShortenedURL.objects.get(shortened_url=shortened_url)
            return Response({"original_url": url.original_url}, status=status.HTTP_302_FOUND)
        except ShortenedURL.DoesNotExist:
            return Response({"error": "URL not found"}, status=status.HTTP_404_NOT_FOUND)

class RedirectView(APIView):
    def get(self, request, shortened_url):
        obj = get_object_or_404(ShortenedURL, shortened_url=shortened_url)
        return redirect(obj.original_url)
