from django.db import models

# Create your models here.

class ABC(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15, null=True, blank=False)


class State(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "State"
    def __str__(self):
        return f"State: {self.state_name}({self.state_id})"


    @classmethod
    def sync(cls):
        from apis.apisetu.apisetu import ApiSetu
        states = ApiSetu().get_states()

        objs = [
            cls(state_id=state.state_id,state_name=state.state_name)
            for state in states
        ]
        cls.objects.bulk_create(objs)


class District(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural =  "District"

    def __str__(self):
        return f"District: {self.district_name}({self.district_id})"

    @classmethod
    def sync(cls):
        from apis.apisetu.apisetu import ApiSetu
        apisetu = ApiSetu()
        states = State.objects.all()
        for state in states:
            districts = apisetu.get_districts(state.state_id)
            objs = [
                cls(district_id=district.district_id,district_name=district.district_name, state=state)

                for district in districts]
            cls.objects.bulk_create(objs)