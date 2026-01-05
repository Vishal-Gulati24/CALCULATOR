import ast
import operator

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import CalculatorSerializer

# Create your views here.

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(node):
    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        return OPS[type(node.op)](left, right)

    if isinstance(node, ast.Num):
        return node.n

    raise ValueError("Invalid expression")


@api_view(['POST'])
def calculate(request):
    serializer = CalculatorSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    expression = serializer.validated_data['expression']

    try:
        tree = ast.parse(expression, mode='eval')
        result = safe_eval(tree.body)
    except Exception:
        return Response(
            {"error": "Invalid or unsafe expression"},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response({"result": result}, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def calculate(request):
#     expression = request.data.get("expression")
#     if not expression:
#         return Response({"error":"expression is Required"},status=status.HTTP_400_BAD_REQUEST)
#     try:
#         result = eval(expression)
#     except Exception:
#         return Response({"error":"invalid expression"},status= status.HTTP_400_BAD_REQUEST)
#     return Response({"result":result},status=status.HTTP_200_OK)
