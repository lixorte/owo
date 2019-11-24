from voluptuous import Schema, Required, In, All, Range

get_last_election = Schema(
    {
        "type": str
    },
    required=True
)

get_election_info = Schema(
    {
        "electionUid": str
    },
    required=True
)

update_election_info = Schema(
    {
        Required("electionUid"): str,
        "name": str,
        "state": In(
            [
                "freezed",
                "ongoing",
                "finished"
            ]
        )
    }
)

delete_election = get_election_info

make_vote = Schema(
    {
        "electionUid": str,
        "voteUid": str,
    },
    required=True
)

edit_option = Schema(
    {
        Required("electionUid"): str,
        Required("voteUid"): str,
        "name": str,
        "singer": str,
        "album": str,
        "state": In(
            [
                "normal",
                "banned"
            ]
        )
    }
)

create_election = Schema(
    {
        "name": str,
        "state": In(
            [
                "normal",
                "banned"
            ]
        ),
        "type": In(
            [
                "topic",
                "song"
            ]
        )
    },
    required=True
)

get_elections = Schema(
    {
        "offset": All(int, Range(min=0)),
        Required("limit"): All(int, Range(min=1, max=100)),
        Required("type", default="any"): In(
            [
                "topic",
                "song",
                "any"
            ]
        )
    }
)

add_option = Schema(
    {
        Required("electionUid"): str,
        Required("name"): str,
        Required("type"): In(
            [
                "topic",
                "song"
            ]
        ),
        "singer": str,
        "cutCommentary": str,
        "album": str,
        "serviceLink": str
    }
)

add_user = Schema(
    {
        "login": str,
        "password": str,
        "ejlogin": str,
        "ejpassword": str
    },
    required=True
)

get_users = Schema(
    {
        "offset": All(int, Range(min=0)),
        Required("limit"): All(int, Range(min=1, max=100)),
        Required("type", default="any"): In(
            [
                "admin",
                "normal",
                "any"
            ]
        )
    }
)

get_user = Schema(
    {
        "userUid": str
    }
)
