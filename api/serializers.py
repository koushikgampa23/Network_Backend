from .models import Nodes, Edges, RouteHistory
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .utils import find_shortest_path


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodes
        fields = "__all__"


class EdgePostSerializer(serializers.ModelSerializer):
    source = serializers.CharField()
    destination = serializers.CharField()

    class Meta:
        model = Edges
        fields = "__all__"

    def validate(self, data):
        source = data.get("source")
        destination = data.get("destination")
        latency = data.get("latency")

        if not source or not destination or latency is None:
            raise ValidationError("Source/Destination/Latency fields are missing")

        if latency <= 0:
            raise ValidationError("Latency must not be less than 0")

        try:
            source_instance = Nodes.objects.get(name=source)
        except Nodes.DoesNotExist:
            raise ValidationError("Source not found in nodes")

        try:
            destination_instance = Nodes.objects.get(name=destination)
        except Nodes.DoesNotExist:
            raise ValidationError("Destination not found in nodes")

        if source_instance == destination_instance:
            raise ValidationError("Source and destination must be different")

        is_duplicate = Edges.objects.filter(
            source=source_instance, destination=destination_instance
        )
        if is_duplicate.exists():
            raise ValidationError("Duplicate Edges")

        data["source"] = source_instance
        data["destination"] = destination_instance

        return data


class EdgeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edges
        fields = "__all__"
        depth = 1


class RouteHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteHistory
        fields = "__all__"
        read_only_fields = [
            "id",
            "total_latency",
            "path",
            "created_at",
        ]

    def create(self, validated_data):
        source = validated_data.get("source")
        destination = validated_data.get("destination")

        try:
            Nodes.objects.get(name=source)
        except Nodes.DoesNotExist:
            raise ValidationError("Source Node doesnot exist")

        try:
            Nodes.objects.get(name=destination)
        except Nodes.DoesNotExist:
            raise ValidationError("Destination Node doesnot exist")

        short_path = find_shortest_path(source, destination)

        if short_path is None:
            return ValidationError(
                {"error": f"No path exists between {source} and {destination}"},
            )

        history_obj = RouteHistory.objects.create(
            source=source,
            destination=destination,
            total_latency=short_path.get("total_latency"),
            path=short_path.get("path"),
        )

        return history_obj


class RouteHistoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteHistory
        fields = "__all__"
