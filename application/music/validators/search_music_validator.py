from marshmallow import Schema, fields, post_load


class SearchMusicValidator(Schema):
    city = fields.String(required=True, allow_none=False)

    @post_load
    def make_data(self, data: dict, **kwargs):
        return data["city"]
