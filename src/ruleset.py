import json
from random import randint, random


class NameSegment(object):
    def __init__(self, segment_type: str, segments: list[str]) -> None:
        assert segments

        self.segment_type = segment_type
        self.segments = segments

    def get_segment(self) -> str:
        i = randint(0, len(self.segments) - 1)
        return self.segments[i]


class Ruleset(object):
    def __init__(
        self,
        name: str,
        name_segments: list[NameSegment],
        name_formats: list[tuple[str, int]],
    ) -> None:
        """
        Used to create a Ruleset manually.
        """

        assert name_segments
        assert name_formats

        self.name = name
        self.name_segments = name_segments
        self.name_formats = name_formats

    @classmethod
    def from_json(cls, ruleset_path: str):
        """
        Used to create a Ruleset from the given JSON filepath.
        """

        data = {}
        with open(ruleset_path, "r") as rs_file:
            data = json.loads(rs_file.read())

        name_segments = []
        for json_name_segment in data["nameSegments"]:
            name_segment = NameSegment(
                json_name_segment["segmentType"], json_name_segment["segments"]
            )
            name_segments.append(name_segment)

        return Ruleset(data["listName"], name_segments, data["nameFormats"])

    def get_name(self) -> str:
        # Choose name format
        chosen_format = self.name_formats[-1]["value"]
        weight_sum = sum(map(lambda x: x["weight"], self.name_formats))
        roll = random() * weight_sum
        for name_format in self.name_formats:
            # Set chosen format and exit if roll is less than weight,
            # otherwise subtract weight from roll and continue.
            if roll < name_format["weight"]:
                chosen_format = name_format["value"]
                break
            roll -= name_format["weight"]

        # Replace segment codes in the chosen name format
        generated_name = chosen_format
        for name_segment in self.name_segments:
            segment_code = "{" + name_segment.segment_type + "}"
            # Replace every instance of the segment code in the name,
            # one at a time so each instance is hopefully different.
            while segment_code in generated_name:
                generated_name = generated_name.replace(
                    segment_code, name_segment.get_segment(), 1
                )

        return generated_name
