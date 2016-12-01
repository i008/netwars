import begin
import rq
from apscheduler.schedulers.blocking import BlockingScheduler
from nw.jobs import update_re_scrape_topics, test_job
from nw.loggers import logger
from nw.nw_redis import NwRedis
from nw.parser import NwParser


class NetwarsBeat(NwParser, NwRedis):
    def __init__(self):
        NwRedis.__init__(self)
        NwParser.__init__(self)

        self.topic_job_queue = rq.Queue(
            connection=self.redis_connection,
            name='scrape_topics',
            default_timeout=200
        )
        self.schedule = BlockingScheduler()

    def one_beat(self):
        logger.info("running beat.")
        topic_status = self.get_topics_from_redis()
        user_status = self.get_users_from_redis()

        if not topic_status or not user_status:
            topics_new, list_of_users = self.home_page_status()
            if topics_new:
                self.save_topics_to_redis(topics_new)
            if list_of_users:
                self.save_users_to_redis(list_of_users)
            return

        elif topic_status and user_status:
            topics_new, list_of_users_new = self.home_page_status()
            topic_diff = self.topic_differences(topic_status, topics_new)
            users_diff = self.live_user_differences(user_status, list_of_users_new)

            # this means that changes on netwars occured between 2 scrapes
            if topic_diff:
                # main job (what to do with the changes)
                logger.debug('in topic diff adding to queue {}'.format(list(topic_diff)))
                self.topic_job_queue.enqueue(update_re_scrape_topics, kwargs={'topic_ids': list(topic_diff)})
                self.save_topics_to_redis(topics_new)

            # this means that online users changed between 2 scrapes
            if users_diff:
                pass

    def start(self, delay):
        self.topic_job_queue.enqueue(test_job)
        self.schedule.add_job(self.one_beat, 'interval', seconds=delay)
        self.schedule.start()


@begin.start(auto_convert=True)
def main(frequency=20):
    """"
    :param frequency: Frequency to check netwars for changes
    :return: None
    """
    NetwarsBeat().start(frequency)
