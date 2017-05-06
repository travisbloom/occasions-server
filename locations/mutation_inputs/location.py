from graphene import String, InputField


class LocationInput(InputField):
    street_address_line1 = String(required=True)
    street_address_line2 = String(required=False)
    postal_code = String(required=True)
    city = String(required=True)
    state = String(required=True)
