from rest_framework import serializers

from user_panel_address_module.model.state import State


class StateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'