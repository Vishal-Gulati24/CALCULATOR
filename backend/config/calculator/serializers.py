from rest_framework import serializers
class CalculatorSerializer(serializers.Serializer):
    expression = serializers.CharField(max_length = 100)