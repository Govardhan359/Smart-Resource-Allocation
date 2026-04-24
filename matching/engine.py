import math
from volunteers.models import Volunteer
from needs.models import Need

def haversine_km(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def match_volunteers_to_need(need_id: int, top_n: int = 5):
    try:
        need = Need.objects.get(id=need_id)
    except Need.DoesNotExist:
        return []

    volunteers = Volunteer.objects.filter(available=True)
    results = []

    for vol in volunteers:
        # Skill match
        vol_skills = [s.lower() for s in vol.skills]
        need_words = need.description.lower().split()
        matches = sum(1 for s in vol_skills if any(s in w for w in need_words))
        skill_score = matches / max(len(vol_skills), 1)

        # Proximity score
        if need.location_lat and need.location_lng:
            dist_km = haversine_km(
                need.location_lat, need.location_lng,
                vol.location_lat, vol.location_lng
            )
        else:
            dist_km = 0

        proximity = 1 / (1 + dist_km)

        # Final score
        final_score = need.urgency_score * (0.5 * skill_score + 0.5 * proximity)

        results.append({
            'volunteer_id': vol.id,
            'volunteer_name': vol.name,
            'volunteer_phone': vol.phone,
            'volunteer_email': vol.email,
            'area_name': vol.area_name,
            'skills': vol.skills,
            'distance_km': round(dist_km, 1),
            'skill_score': round(skill_score, 3),
            'match_score': round(final_score, 3),
        })

    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results[:top_n]