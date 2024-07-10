from djongo import models

# class TestModel(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()

#     class Meta:
#         abstract = False

class YourModel(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    written_id = models.CharField(max_length = 255)
    coffee_id = models.CharField(max_length=255)
    note_floral = models.BooleanField(default=False)
    note_fruit = models.BooleanField(default=False)
    note_berry = models.BooleanField(default=False)
    note_nut = models.BooleanField(default=False)
    note_choco = models.BooleanField(default=False)
    note_cereal = models.BooleanField(default=False)
    taste_sweet = models.IntegerField()
    taste_sour = models.IntegerField()
    taste_bitter = models.IntegerField()
    taste_body = models.IntegerField()
    overall_score = models.IntegerField()
    feeling = models.CharField(max_length=255)

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.id} - {self.feeling}"


class User(models.Model):
    id = models.CharField(primary_key=True,max_length=255)
    name = models.CharField(max_length=255)
    review_lst = models.JSONField(default=list)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Coffee(models.Model):
    _id = models.ObjectIdField()
    type = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    name_eng = models.CharField(max_length=255)
    script = models.TextField()
    review_lst = models.JSONField(default=list)

    def __str__(self):
        return f"{self.id} - {self.name}"