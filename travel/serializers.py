from rest_framework import serializers


class TopDistrictSerializer(serializers.Serializer):
    district = serializers.CharField()
    avg_temperature = serializers.FloatField()
    avg_air_quality = serializers.FloatField()


class RecommendTravelSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    destination_district = serializers.CharField()
    travel_date = serializers.DateField()
