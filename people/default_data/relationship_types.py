from people.models import RelationshipType

relationships_types_initial_data = {
    "friend_to_friend": {
        "from_person_male_display_name": "Friend"
    },
    "monogamous": {
        "from_person_male_display_name": "Boyfriend",
        "from_person_female_display_name": "Girlfriend",
    },
    "sibling_to_sibling": {
        "from_person_male_display_name": "Brother",
        "from_person_female_display_name": "Sister",
    },
    "parent_to_child": {
        "from_person_male_display_name": "Father",
        "from_person_female_display_name": "Mother",
        "to_person_male_display_name": "Son",
        "to_person_female_display_name": "Daughter",
    },
    "grandparent_to_grandchild": {
        "from_person_male_display_name": "Grandfather",
        "from_person_female_display_name": "Grandmother",
        "to_person_male_display_name": "Grandson",
        "to_person_female_display_name": "Granddaughter",
    },
}


def generate_default_relationship_types():
    relationships =  [
        RelationshipType(pk=key, **value)
        for key, value in relationships_types_initial_data.items()
    ]
    [relationship.save() for relationship in relationships]
    return relationships

