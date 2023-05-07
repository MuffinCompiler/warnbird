# Custom logger to write and read already posted events.
# Required as state to not post warning more than once.
# Also has handles to tweets, to post answers if necessary

class PostingLogger:

    def __init__(self, fp):

        self.local_log = []
        self.log_fp = fp


    def post(self, post):

        self.local_log.append(post)

        pass

    def already_posted(self, event):
        print("todo check if already posted")
        return False
        # TODO
        # check if in local cache
        if event in self.local_log:
            return True

        # if not, consult log file. if there, load it for reference
        handle = open(self.log_fp)
        posted = handle.read()
        if event in posted:
            self.local_log.append(event)
            return True

        return False