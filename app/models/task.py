from django.db import models


class Task(models.Model):
    id = models.CharField(max_length=36, primary_key=True, unique=True)
    name = models.CharField(max_length=128, db_index=True, null=False)
    description = models.CharField(max_length=128)
    profile_id = models.PositiveIntegerField(null=False)
    complete = models.BooleanField(default=False)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.profile_id == other.profile_id
            and self.complete == other.complete
        )
