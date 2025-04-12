import polars as pl
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import utils
from .models import District
from .serializers import TopDistrictSerializer, RecommendTravelSerializer


class TopDistrictsView(APIView):
    def get(self, requests):
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
