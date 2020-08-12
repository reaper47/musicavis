from django.db import models


class EmailPreferences(models.Model):
    features = models.BooleanField(default=True)
    practicing = models.BooleanField(default=True)
    promotions = models.BooleanField(default=True)

    def __eq__(self, other):
        return (
            self.features == other.features
            and self.practicing == other.practicing
            and self.promotions == other.promotions
        )

    def __hash__(self):
        return hash(self.features + self.practicing + self.promotions)

    def __str__(self):
        return f"[{self.features},{self.practicing},{self.promotions}]"
