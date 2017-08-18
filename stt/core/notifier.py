# -*- coding: utf-8 -*-
#**********************************************************
#* CATEGORY    JARVIS HOME AUTOMTION
#* GROUP       SPEECH TO TEXT
#* AUTHOR      LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#**********************************************************
#Jarvis Home Automation
#Copyright (C) 2017  Haynie Research & Development

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import Queue
import atexit
from modules import Gmail
from apscheduler.schedulers.background import BackgroundScheduler
import logging


class Notifier(object):

    class NotificationClient(object):

        def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp

        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self, profile):
        self._logger = logging.getLogger(__name__)
        self.q = Queue.Queue()
        self.profile = profile
        self.notifiers = []

        if 'gmail_address' in profile and 'gmail_password' in profile:
            self.notifiers.append(self.NotificationClient(
                self.handle_email_notifications, None))
        else:
            self._logger.warning('gmail_address or gmail_password not set ' +
                                 'in profile, Gmail notifier will not be used')

        sched = BackgroundScheduler(timezone="UTC", daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=30)
        atexit.register(lambda: sched.shutdown(wait=False))

    def gather(self):
        [client.run() for client in self.notifiers]

    def handle_email_notifications(self, last_date):
        """Places new Gmail notifications in the Notifier's queue."""
        emails = Gmail.fetch_unread_emails(self.profile, since=last_date)
        if emails:
            last_date = Gmail.get_most_recent_date(emails)

        def style_email(e):
            return "New email from %s." % Gmail.get_sender(e)

        for e in emails:
            self.q.put(style_email(e))

        return last_date

    def get_notification(self):
        """Returns a notification. Note that this function is consuming."""
        try:
            notif = self.q.get(block=False)
            return notif
        except Queue.Empty:
            return None

    def get_all_notifications(self):
        """
            Return a list of notifications in chronological order.
            Note that this function is consuming, so consecutive calls
            will yield different results.
        """
        notifs = []

        notif = self.get_notification()
        while notif:
            notifs.append(notif)
            notif = self.get_notification()

        return notifs
