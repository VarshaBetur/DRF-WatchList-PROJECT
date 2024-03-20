from watchlist_app.models import Movie, StreamPlatform, WatchList, Review
from rest_framework import serializers

# serializers.Serializer

# def description_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too small")
#     else:
#         return value
#
# class MovieSerializers(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField()
#     description=serializers.CharField(validators=[description_length])
#     active=serializers.BooleanField(default=True,write_only=True)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         """
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Movie` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#     # type of Serializer validations
#
#     #field level validation
#     def validate_name(self, value):
#         if len(value)<2:
#             raise serializers.ValidationError("Name is too small")
#         else:
#             return value
#
#     # object level validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Descriptionis should not be same")
#         else:
#             return data

#ModelSerializer
class MovieSerializers(serializers.ModelSerializer):
    name_len=serializers.SerializerMethodField()

    class Meta:
        model=Movie
        # fields="__all__"
        # fields=['name','description']
        exclude=['active']

    def get_name_len(self, object):
        return len(object.name)

    # field level validation
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too small")
        else:
            return value

    # object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and Descriptionis should not be same")
        else:
            return data


class ReviewSerializers(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        # fields="__all__"
        exclude=('watchlist',)

class WatchListSerializers(serializers.ModelSerializer):
    # reviews = ReviewSerializers(many=True, read_only=True) #no need to give review while creating a watchlist because read_only=True
    # average_rating=serializers.SerializerMethodField()
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model=WatchList
        fields=[
            "id",
            "title",
            "story_line",
            "platform",
            "active",
            "created",
            # "reviews",
            # "average_rating",
            "avg_rating",
            "number_rating"
        ]

    def get_average_rating(self, object):
        reviews_list = object.reviews.all().values_list("rating",flat=True)
        if len(reviews_list)>0:
            average_rating=sum(reviews_list)/len(reviews_list)
            return average_rating
        return 0

# class StreamPlatformSerializers(serializers.HyperlinkedModelSerializer):
class StreamPlatformSerializers(serializers.ModelSerializer):
    watchlist= WatchListSerializers(many=True, read_only=True) #related name for Platform is watchlist in WatchList model
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="watch-list-details")  #url to see the watchlist details
    # watchlist = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='story_line'
    # )
    # watchlist = serializers.HyperlinkedIdentityField(many=True, view_name="watch-list-details")
    class Meta:
        model=StreamPlatform
        fields="__all__"
