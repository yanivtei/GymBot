# encoding: utf-8
from __future__ import unicode_literals

import logging
import os

from telegram.ext import Updater

from gym_bot_app.commands import (AdminCommand,
                                  MyDaysCommand,
                                  TrainedCommand,
                                  SelectDaysCommand,
                                  MyStatisticsCommand,
                                  AllTrainingTraineesCommand)

from gym_bot_app.commands.set_reminder import SetReminderCommand

from gym_bot_app.tasks import (GoToGymTask,
                               WentToGymTask,
                               NewWeekSelectDaysTask)


MSG_TIMEOUT = 20

logging.basicConfig(filename='logs/gymbot.log',
                    encoding='utf-8',
                    format='%(asctime)s %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)


def run_gym_bot(token, logger):
    updater = Updater(token=token)

    """ Tasks """
    GoToGymTask(updater=updater, logger=logger).start()
    WentToGymTask(updater=updater, logger=logger).start()
    NewWeekSelectDaysTask(updater=updater, logger=logger).start()

    """ Commands """
    AdminCommand(updater=updater, logger=logger).start()
    MyDaysCommand(updater=updater, logger=logger).start()
    TrainedCommand(updater=updater, logger=logger).start()
    SelectDaysCommand(updater=updater, logger=logger).start()
    SetReminderCommand(updater=updater, logger=logger).start(command_name='set_reminder')
    MyStatisticsCommand(updater=updater, logger=logger).start()
    AllTrainingTraineesCommand(updater=updater, logger=logger).start(command_name='all_the_botim')

    updater.start_polling(timeout=MSG_TIMEOUT)
    updater.idle()


if __name__ == '__main__':
    import sys

    # if len(sys.argv) > 1 and sys.argv[1] == 'test':
    #     os.environ['BOT_TOKEN'] = os.environ['BOT_TOKEN_TEST']
    #     os.environ['MONGODB_URL_CON'] = os.environ['MONGODB_URL_CON_TEST']
    #
    # token = os.environ['BOT_TOKEN']
    # db_con_string = os.environ['MONGODB_URL_CON']
    token = '664741071:AAFXrWOwpPP3Tvf_quwz8RgPBmGMUEWg2eI'
    db_con_string = 'mongodb://yaniv:yaniv4197@ds147964.mlab.com:47964/teicherbottest'

    from mongoengine import connect
    connect(host=db_con_string)

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())

    run_gym_bot(token, logger)
