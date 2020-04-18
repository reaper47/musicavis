from typing import Dict, List
from app.models.practice import Goal, Exercise, Positive, Improvement


class PracticeDTO:
    __slots__ = ["goals", "exercises", "positives", "improvements", "notes"]

    def __init__(
        self,
        goals: List[Goal],
        exercises: List[Exercise],
        positives: List[Positive],
        improvements: List[Improvement],
        notes: str,
    ):
        self.goals = goals
        self.exercises = exercises
        self.positives = positives
        self.improvements = improvements
        self.notes = notes

    @staticmethod
    def model_to_jsonable(model, toast: str):
        return {
            "goals": [x.name.capitalize() for x in model.goals.all()],
            "positives": [x.name.capitalize() for x in model.positives.all()],
            "improvements": [x.name.capitalize() for x in model.improvements.all()],
            "exercises": [
                {
                    "name": x.name.title(),
                    "bpm_start": x.bpm_start,
                    "bpm_end": x.bpm_end,
                    "minutes": x.minutes,
                }
                for x in model.exercises.all()
            ],
            "notes": model.notes,
            "toast": toast,
        }

    @staticmethod
    def json_to_model(json: Dict[str, str]):
        goals = PracticeDTO.__find_or_create_name_entities(json["goals"], Goal)
        exercises = PracticeDTO.__find_or_create_exercise_entities(json["exercises"])
        positives = PracticeDTO.__find_or_create_name_entities(
            json["positives"], Positive
        )
        improvements = PracticeDTO.__find_or_create_name_entities(
            json["improvements"], Improvement
        )
        notes = json["notes"] if json["notes"] else None

        return PracticeDTO(
            list(set(goals)),
            list(set(exercises)),
            list(set(positives)),
            list(set(improvements)),
            notes,
        )

    @classmethod
    def __find_or_create_name_entities(cls, names, entity):
        entities = []
        for name in [x["name"].lower() for x in names if x["name"]]:
            x = entity.objects.filter(name=name).first()
            if x is None:
                x = entity.objects.create(name=name)
            entities.append(x)
        return entities

    @classmethod
    def __find_or_create_exercise_entities(cls, exercises):
        entities = []
        exercises = [
            x
            for x in exercises
            if x["name"] and x["bpm_start"] and x["bpm_end"] and x["minutes"]
        ]
        for exercise in exercises:
            name, start, end, minutes = (
                exercise["name"],
                exercise["bpm_start"],
                exercise["bpm_end"],
                exercise["minutes"],
            )
            entity = Exercise.objects.filter(
                name=name.lower(), bpm_start=start, bpm_end=end, minutes=minutes
            ).first()
            if entity is None:
                entity = Exercise.objects.create(
                    name=name.lower(), bpm_start=start, bpm_end=end, minutes=minutes
                )
            entities.append(entity)
        return entities

    def __eq__(self, other):
        return (
            set([x.name for x in self.goals]) == set([x.name for x in other.goals])
            and sorted(self.exercises) == sorted(other.exercises)
            and set([x.name for x in self.improvements])
            == set([x.name for x in other.improvements])
            and set([x.name for x in self.positives])
            == set([x.name for x in other.positives])
        )
