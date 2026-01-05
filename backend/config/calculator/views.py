from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(["POST"])
def calculate(request):
    expression = request.data.get("expression")
    if not expression:
        return Response({"error":"expression is Required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        result = eval(expression)
    except Exception:
        return Response({"error":"invalid expression"},status= status.HTTP_400_BAD_REQUEST)
    return Response({"result":result},status=status.HTTP_200_OK)
