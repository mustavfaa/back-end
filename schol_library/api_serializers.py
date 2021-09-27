from schol_library import models
from rest_framework import serializers


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.p_models.AlmaMater
        fields = ('id', 'name')

class EditionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    language = serializers.CharField()
    klass = serializers.CharField()
    author = serializers.CharField()
    publisher = serializers.CharField()
    series_by_year = serializers.CharField()
    publish_date = serializers.CharField()
    metodology_complex = serializers.CharField()
    isbn = serializers.CharField()
    subject = serializers.CharField()
    study_direction = serializers.CharField()
    summ = serializers.IntegerField(default=0, allow_null=True)
    in_warehouse = serializers.IntegerField(default=0, allow_null=True)


class NumberBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NumberBooks
        fields = ('edition', 'summ', 'in_warehouse', 'school', 'it_filled')


class NumberBooksLibrianGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NumberBooks
        fields = ('id', 'edition', 'results', 'school', 'it_filled', 'in_warehouse', 'summ')