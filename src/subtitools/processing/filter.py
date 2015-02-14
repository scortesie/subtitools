class Filter(object):
    def __init__(self):
        pass

    def filter(self, subtitle):
        raise NotImplementedError()


class HideTextFilter(Filter):
    def __init__(self, percentage_to_hide):
        Filter.__init__(self)
        self.percentage_to_hide = percentage_to_hide

    def filter(self, subtitle):
        pass
