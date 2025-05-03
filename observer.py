class TopicAccessObserver:
    def __init__(self):
        self.topic_counts = {}

    def access_topic(self, topic_id):
        self.topic_counts[topic_id] = self.topic_counts.get(topic_id, 0) + 1

    def get_stats(self):
        return self.topic_counts