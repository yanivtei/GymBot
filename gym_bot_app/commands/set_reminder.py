# encoding: utf-8
from __future__ import unicode_literals

import argparse
from datetime import datetime

from gym_bot_app.commands import Command
from gym_bot_app.decorators import get_trainee_and_group
from gym_bot_app.tasks.personal_go_to_gym import PersonalGoToGymTask


class SetReminderCommand(Command):

    INPUT_TIME_FORMAT = "%H:%M"
    WRONG_TIME_FORMAT_MESSAGE = 'זה לא בפורמט יא בוט, נסה שוב'

    def __init__(self, *args, **kwargs):
        super(SetReminderCommand, self).__init__(*args, **kwargs)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('reminder_time')


    @get_trainee_and_group
    def _handler(self, bot, update, trainee, group):

        self.logger.info('Set reminder command with %s in %s', trainee, group)


        try:
            args = self.parser.parse_args()
            reminder_time = datetime.strptime(args['reminder_time'], self.INPUT_TIME_FORMAT)
            training_days = [day.name for day in trainee.training_days.filter(selected=True)]
            for day in training_days:
                PersonalGoToGymTask(self.updater, self.logger, trainee, day, reminder_time).start()

        except ValueError as e:
            self.logger.error('Failed to execute command due wrong input time format, exception: %s', e)
            update.message.reply_text(qoute=True, text=self.WRONG_TIME_FORMAT_MESSAGE)

    def start(self, *args, **kwargs):
        kwargs['pass_args'] = True
        return super(SetReminderCommand, self).start(*args, **kwargs)
