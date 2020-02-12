from rest_framework import serializers

from fs.models import Rtz


class RtzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rtz
        # fields = '__all__'
        fields = ('id', 'doc_id', 'family', 'person_name', 'tags', 'views', 'comments', 'marks')
