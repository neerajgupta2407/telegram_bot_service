from django.db import models
import telegram
from app.utils import lis_to_str, lis_to_str_with_indx, insert_top
from app.config import *


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

class TelegramUser(models.Model):
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=50)
    chat_id = models.CharField(max_length=20)
    saved_alerts = models.JSONField(null=True, blank=True)
    recent_searches = models.JSONField(null=True, blank=True)
    alerts_18 = models.PositiveIntegerField(default=0)
    alerts_45 = models.PositiveIntegerField(default=0)
    total_alerts_18 = models.PositiveIntegerField(default=0)
    total_alerts_45 = models.PositiveIntegerField(default=0)

    @classmethod
    def subscribe(cls, chat_id, username, ):
        """
        Sunscribe To telegram.
        :param chat_id:
        :param username:
        :return:
        """
        obj, _ = cls.objects.get_or_create(chat_id=chat_id)
        obj.username = username[:50]
        obj.save()
        return obj

    def save_search_query(self, query):
        # Saving the terms search by User on Telegram.
        self.recent_searches = self.recent_searches or []
        self.recent_searches = insert_top(self.recent_searches, query)
        self.save()

    def get_recent_searches(self, last_n_searches=SHOW_LAST_N_SEARCH):
        # Returns last n searches of User.
        lis = self.recent_searches or []
        return lis[:last_n_searches]

    def save_alert(self, age_type, **kwargs):
        # Saving the alerts requested by USer.
        # {18:{district_ids:[1,2,3,45,]}}
        district_id = kwargs.get("district_id")
        dic = self.saved_alerts or {}
        dic[age_type] = dic.get(age_type, {})
        if district_id:
            dic[age_type][CONST_DISTRICT_IDS] = dic[age_type].get(
                CONST_DISTRICT_IDS, []
            )
            dic[age_type][CONST_DISTRICT_IDS] = insert_top(
                dic[age_type][CONST_DISTRICT_IDS], district_id
            )
        self.saved_alerts = dic
        self.is_active = True
        return self.save()

    @property
    def get_saved_alerts_str(self):
        # Returns the Beautiful String for the saved alerts of User.
        lis = []
        if self.saved_alerts:
            msg = "Below are the subscribed alerts."
            for age, val in self.saved_alerts.items():
                # st = f"{age}+\n"
                dist_ids = val.get(CONST_DISTRICT_IDS, [])
                if dist_ids:
                    dist_names = list(
                        District.objects.filter(pk__in=dist_ids).values_list(
                            "district_name", flat=True
                        )
                    )
                    lis.append(f"{age}+ Districts: {', '.join(dist_names)}")
        else:
            msg = "You are not subscribed for any Alerts"
        return lis_to_str([msg, lis_to_str_with_indx(lis)])

    def send_message(self, msg):
        # Sending message to user.
        telegram_bot = telegram.Bot(token=telegram_token)
        try:
            max_size = 4000
            if len(msg) > max_size:
                chunks = [msg[i : i + max_size] for i in range(0, len(msg), max_size)]
                for msg in chunks:
                    telegram_bot.send_message(
                        chat_id=self.chat_id,
                        text=msg,
                        parse_mode=telegram.ParseMode.HTML,
                    )
            else:
                telegram_bot.send_message(
                    chat_id=self.chat_id, text=msg, parse_mode=telegram.ParseMode.HTML
                )
        except telegram.error.Unauthorized:
            # Deactivating the user..
            self.is_active = False
            self.save()
