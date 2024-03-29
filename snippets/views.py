# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Snippet
from .serializers import SnippetSerializer

@api_view(['GET','POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # print('POST - input: {:s}'.format(request.data))
        print(request.data) # {'code': 'print(456)', 'language': 'java'}
        print(request.data["code"])
        print(request.data["language"])
        serializer = SnippetSerializer(data=request.data)

        if serializer.is_valid():
            print(type(serializer.validated_data))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # serializer.data is an OrderedDict object
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def profile_list(request, format=None):

    if request.method == 'GET':
        x = '{ "name":"John", "age":30, "city":"New York"}'
        return Response(x)

    elif request.method == 'POST':
        # print('POST - input: {:s}'.format(request.data))
        print(request.data) # {'code': 'print(456)', 'language': 'java'}
        x = '{ "hobby":"tennis"}'
        x = {} # dictionary
        x['a'] = 'A'
        x['b'] = 'B'
        return Response(x)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)