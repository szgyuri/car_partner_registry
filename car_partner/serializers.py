from rest_framework import serializers

from .models import Partner, Car


class CarSerializer(serializers.ModelSerializer):
    partners = serializers.SerializerMethodField('get_partners')

    def get_partners(self, obj):
        wrapped = self.context.get('wrapped')
        if wrapped is True or wrapped is None:
            return [partner.id for partner in obj.partners.all()]
        else:
            return [PartnerSerializer(partner).data for partner in obj.partners.all()]

    class Meta:
        model = Car
        fields = ('id', 'average_fuel', 'delegation_starting', 'delegation_ending', 'driver', 'owner', 'type',
                  'partners', 'created_at', 'modified_at', 'deleted_at')


class PartnerSerializer(serializers.ModelSerializer):
    cars = serializers.SerializerMethodField('get_cars')

    def get_cars(self, obj):
        wrapped = self.context.get('wrapped')
        if wrapped is True or wrapped is None:
            return [car.id for car in obj.cars_set.all()]
        else:
            return [CarSerializer(car).data for car in obj.cars_set.all()]

    class Meta:
        model = Partner
        fields = ('id', 'name', 'city', 'address', 'company_name', 'cars', 'created_at', 'modified_at', 'deleted_at')


class CarPartnerSerializer(serializers.Serializer):
    partner_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1)
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
