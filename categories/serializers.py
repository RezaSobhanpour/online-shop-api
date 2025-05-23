from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Category.objects.all(), required=False,
                                                allow_null=True)
    parent_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'parent_title', 'description', 'created_at', 'updated_at',
                  'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_parent_title(self, obj):
        return obj.parent.title if obj.parent else None

    def validate_parent(self, value):
        if value and self.instance and value.id == self.instance.id:
            raise serializers.ValidationError("A category cannot be its own parent.")
