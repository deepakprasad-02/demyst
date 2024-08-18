import json


class Spec:
    def __init__(self, spec_data: dict):
        self.column_names = spec_data["ColumnNames"]
        self.offsets = list(map(int, spec_data["Offsets"]))
        self.fixed_width_encoding = spec_data["FixedWidthEncoding"]
        self.include_header = spec_data.get("IncludeHeader", "False") == "True"
        self.delimited_encoding = spec_data["DelimitedEncoding"]

    @classmethod
    def from_json(cls, json_file: str) -> "Spec":
        with open(json_file, "r") as f:
            spec_data = json.load(f)
        return cls(spec_data)
