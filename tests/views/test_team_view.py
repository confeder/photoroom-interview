"""Tests for /api/teams/*

Some ideas for more test cases:

- Verify GET /api/teams/<id>
- Verify all the views demand authentication
- Verify view checks against Django permissions
- Verify content negotiation
- Verify authentication scheme
- Verify team name validation
- Verify joining/leaving non-existent team
- Verify updating/deleting non-existent team
"""

from anys import ANY_INT
from django.contrib.auth.models import Group


def test_team_view_only_lists_members_user_is_member_of(user_a, user_a_client):
    member_team = Group.objects.create(name="teamA")
    Group.objects.create(name="teamB")

    user_a.groups.add(member_team)

    response = user_a_client.get("/api/teams/")
    assert response.json() == [
        {
            "id": member_team.id,
            "name": member_team.name,
            "users": [
                {
                    "id": user_a.id,
                    "email": user_a.email,
                }
            ],
        },
    ]


def test_team_view_allows_creating_team(user_a, user_a_client):
    response = user_a_client.post(
        "/api/teams/",
        data={
            "name": "myteam",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": ANY_INT,
        "name": "myteam",
        "users": [
            {
                "id": user_a.id,
                "email": user_a.email,
            },
        ],
    }

    group = Group.objects.get(id=response.json()["id"])
    assert group.name == "myteam"

    assert group in user_a.groups.all()


def test_team_view_does_not_allow_duplicate_teams(user_a, user_a_client):
    response = user_a_client.post(
        "/api/teams/",
        data={
            "name": "myteam",
        },
        format="json",
    )

    assert response.status_code == 201

    response = user_a_client.post(
        "/api/teams/",
        data={
            "name": "myteam",
        },
        format="json",
    )

    assert response.status_code == 400


def test_team_view_allows_changing_team_name(user_a, user_a_client):
    team = Group.objects.create(name="teamA")
    user_a.groups.add(team)

    response = user_a_client.patch(
        f"/api/teams/{team.id}/", data={"name": "teamB"}, format="json"
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": team.id,
        "name": "teamB",
        "users": [
            {
                "id": user_a.id,
                "email": user_a.email,
            }
        ],
    }

    team.refresh_from_db()
    assert team.name == "teamB"


def test_team_view_does_not_allow_changing_other_teams_name(user_a, user_a_client):
    team = Group.objects.create(name="teamA")

    response = user_a_client.patch(
        f"/api/teams/{team.id}/", data={"name": "teamB"}, format="json"
    )
    assert response.status_code == 404

    team.refresh_from_db()
    assert team.name == "teamA"


def test_team_view_allows_joining_a_team(user_a, user_a_client):
    team = Group.objects.create(name="teamA")

    response = user_a_client.put(f"/api/teams/{team.id}/membership/")
    assert response.status_code == 204

    assert team in user_a.groups.all()


def test_team_view_allows_leaving_a_team(user_a, user_a_client):
    team = Group.objects.create(name="teamA")
    user_a.groups.add(team)

    response = user_a_client.delete(f"/api/teams/{team.id}/membership/")
    assert response.status_code == 204

    assert team not in user_a.groups.all()
