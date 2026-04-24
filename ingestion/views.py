from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from needs.models import Need
from .gemini_service import parse_field_report


class UploadReportView(APIView):
    def post(self, request):
        text = request.data.get("text", "").strip()
        if not text:
            return Response(
                {"error": "No report text provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            parsed_needs = parse_field_report(text)
        except Exception as e:
            return Response(
                {"error": f"AI parsing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not parsed_needs:
            return Response(
                {"error": "No needs could be extracted from the report."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        created = []
        for item in parsed_needs:
            need = Need.objects.create(
                title=item.get("title", "Untitled Need"),
                description=item.get("description", ""),
                category=item.get("category", "other"),
                urgency_score=int(item.get("urgency_score", 5)),
                area_name=item.get("area_name", "Unknown"),
                source_text=text,
                status="open",
            )
            created.append({
                "id": need.id,
                "title": need.title,
                "category": need.category,
                "urgency_score": need.urgency_score,
                "area_name": need.area_name,
            })

        return Response({
            "message": f"{len(created)} need(s) extracted and created.",
            "needs": created
        }, status=status.HTTP_201_CREATED)