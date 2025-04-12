import polars as pl
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import utils
from .models import District
from .serializers import TopDistrictSerializer, RecommendTravelSerializer


class TopDistrictsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        df_list = []

        for district in District.objects.all():
            weather_df = utils.fetch_weather_data(district.lat, district.long)
            air_quality_df = utils.fetch_air_quality_data(district.lat, district.long)
            df = weather_df.join(air_quality_df, on="date", how="inner")
            df = df.with_columns(pl.lit(district.name).alias("district"))
            df_list.append(df)

        combine_df = pl.concat(df_list)
        top_10 = (
            combine_df.select(["district", "avg_temperature", "avg_air_quality"])
            .unique()
            .sort(["avg_temperature", "avg_air_quality"])
            .head(10)
            .to_dicts()
        )

        serializer = TopDistrictSerializer(top_10, many=True)

        return Response(serializer.data)


class RecommendTravelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RecommendTravelSerializer(data=request.data)
        if serializer.is_valid():
            current_lat = serializer.validated_data["latitude"]
            current_long = serializer.validated_data["longitude"]
            dest_dist = serializer.validated_data["destination_district"]

            district = District.objects.filter(name__iexact=dest_dist)
            if district.exists():
                district = district.first()

                current_weather_df = utils.fetch_weather_data(current_lat, current_long)
                current_air_quality_df = utils.fetch_air_quality_data(
                    current_lat, current_long
                )

                dest_weather_df = utils.fetch_weather_data(district.lat, district.long)
                dest_air_quality_df = utils.fetch_air_quality_data(
                    district.lat, district.long
                )

                curr_temp = current_weather_df[0, "avg_temperature"]
                curr_air = current_air_quality_df[0, "avg_air_quality"]
                dest_temp = dest_weather_df[0, "avg_temperature"]
                dest_air = dest_air_quality_df[0, "avg_air_quality"]

                if dest_temp < curr_temp and dest_air < curr_air:
                    resp = {
                        "recommendation": "Recommended",
                        "reason": f"Your destination is {curr_temp - dest_temp:.1f}°C cooler and has better air quality. Enjoy your trip!",
                    }
                else:
                    resp = {
                        "recommendation": "Not Recommended",
                        "reason": "Your destination is hotter or has worse air quality than your current location. It’s better to stay where you are.",
                    }
            else:
                return Response(
                    {"status": "failed", "message": "Destination district not found."}
                )
            return Response(resp)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
