class IntervalCollection:
    total_space_occupied = 0
    number_of_unique_intervals = 0
    number_of_total_intervals = 0

    def __init__(self):
        self.intervals = []
        self.total_space_occupied = 0
        self.sorted = True

    # Appends an item at the end of the collection, this will make the collection unsorted
    def append(self, interval):
        assert(len(interval) == 2)
        assert(interval[0] < interval[1])
        self.sorted = False
        left, right = interval
        if not self.contains(interval):
            self.total_space_occupied += right - left
            self.number_of_unique_intervals += 1
        self.number_of_total_intervals += 1
        self.intervals.append((left, right, right-left))

    def append_sorted(self, interval):
        assert(len(interval) == 2)
        assert self.sorted
        left, right = interval
        i = 0
        while i < len(self.intervals) and self.intervals[i][0] < left:
            i += 1
        if not self.contains(interval):
            self.total_space_occupied += right - left
            self.number_of_unique_intervals += 1
        self.number_of_total_intervals += 1
        self.intervals.insert(i, (left, right, right - left))

    def contains(self, item):
        for i in range(len(self.intervals)):
            if self.intervals[i][0] == item[0] and self.intervals[i][1] == item[1]:
                return True
        return False

    def is_in_interval(self, value):
        for i in range(len(self.intervals)):
            if self.intervals[i][0] <= value < self.intervals[i][1]:
                return True
            if self.sorted:
                if value > self.intervals[i][1]:
                    return False
        return False

    def scale_value(self, value):
        assert self.sorted
        i = 0
        while i < len(self.intervals) and value > self.intervals[i][0]:
            value += self.intervals[i][2]
            i += 1
        return value

    def get_interval_list(self):
        return self.intervals
