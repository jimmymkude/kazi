from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        # fields = ('image', 'title', 'description', 'link', 'company', 'lifetime_in_days')
        fields = '__all__'