from rest_framework import serializers
from customers.models import Customer

#this describe how to serialize it 
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
