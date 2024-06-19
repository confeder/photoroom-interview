"""Tests for /api/palletes/*

Some ideas for more test cases:

- Verify GET /api/palletes/<id>, make sure you can only view YOUR palletes
- Verify all the views demand authentication
- Verify view checks against Django permissions
- Verify content negotiation
- Verify authentication scheme
- Verify color HEX code validation
- Verify that the HEX code is stored in a consistent format, regardless
of how the user specified it.
- Verify updating pallete name and team ownership. You shouldn't be
able to change the ownership to that of a team you are not a member of.
"""

from anys import ANY_INT, ANY_LIST
from django.contrib.auth.models import Group

from photoroom.models import ColorPallete


def test_color_pallete_view_create_pallete(user_a, user_a_client):
    team = Group.objects.create(name="teamA")
    user_a.groups.add(team)

    response = user_a_client.post(
        "/api/palletes/",
        data={
            "name": "mycolors",
            "colors": ["#ffffff"],
            "owner_id": team.id,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": ANY_INT,
        "name": "mycolors",
        "colors": ["#ffffff"],
        "owner": {
            "id": team.id,
            "name": team.name,
            "users": ANY_LIST,
        },
    }

    color_pallete = ColorPallete.objects.select_related("owner").get(
        id=response.json()["id"]
    )
    assert color_pallete.name == "mycolors"
    assert color_pallete.colors == ["#ffffff"]
    assert color_pallete.owner == team


def test_color_pallete_view_create_pallete_against_non_member_team(
    user_a, user_a_client
):
    team = Group.objects.create(name="teamA")

    response = user_a_client.post(
        "/api/palletes/",
        data={
            "name": "mycolors",
            "colors": ["#ffffff"],
            "owner_id": team.id,
        },
        format="json",
    )

    assert response.status_code == 400

    assert not ColorPallete.objects.filter(name="mycolors").exists()


def test_color_pallete_view_list_my_palletes(user_a, user_a_client):
    [team_a, team_b] = Group.objects.bulk_create(
        [Group(name="teamA"), Group(name="teamB")]
    )
    user_a.groups.add(team_a)

    [pallete_a, pallete_b] = ColorPallete.objects.bulk_create(
        [
            ColorPallete(
                name="mycolorsA",
                colors=["#fffff", "#000000"],
                owner=team_a,
            ),
            ColorPallete(
                name="mycolorsB",
                colors=["#fffff", "#000000"],
                owner=team_b,
            ),
        ]
    )

    response = user_a_client.get("/api/palletes/")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": pallete_a.id,
            "name": pallete_a.name,
            "colors": pallete_a.colors,
            "owner": {
                "id": team_a.id,
                "name": team_a.name,
                "users": ANY_LIST,
            },
        }
    ]
