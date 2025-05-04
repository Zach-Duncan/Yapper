class TopicAccessObserver:
    def __init__(self):
        self.access_log = {}

    def notify(self, topic_id):
        if topic_id not in self.access_log:
            self.access_log[topic_id] = 0
        self.access_log[topic_id] += 1

    def get_stats(self):
        return self.access_log
