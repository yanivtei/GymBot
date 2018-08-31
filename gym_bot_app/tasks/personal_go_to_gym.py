# encoding: utf-8
from __future__ import unicode_literals

from gym_bot_app.tasks import Task
from gym_bot_app.tasks.go_to_gym import GoToGymTask


class PersonalGoToGymTask(Task):
    """Telegram gym bot personal go to gym task."""
    DEFAULT_TARGET_TIME = GoToGymTask.DEFAULT_TARGET_TIME
    GO_TO_GYM_INDIVIDUAL = GoToGymTask.GO_TO_GYM_INDIVIDUAL

    def __init__(self, trainee, target_day_name, target_time=None, *args, **kwargs):
        super(PersonalGoToGymTask, self).__init__(*args, **kwargs)
        self.target_time = target_time or self.DEFAULT_TARGET_TIME
        self.target_day_name = target_day_name
        self.trainee = trainee

    def get_start_time(self):
        """Start time of personal go to gym task based on the target time."""
        return self._seconds_until_day_and_time(target_time=self.target_time,
                                                target_day_name=self.target_day_name)

    def execute(self):
        """Override method to execute personal go to gym task.

        Sends personal go to gym message to the given trainee

        """
        self.logger.info('Executing go to gym task with %s', self.trainee)

        go_to_gym_msg = self.GO_TO_GYM_INDIVIDUAL.format(trainees=self.trainee.first_name)
        self.updater.bot.send_message(chat_id=self.trainee.id, text=go_to_gym_msg)
