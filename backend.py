# The field that the simulation occurs on
class Grid:
    # Constructor
    def __init__(self, n_rows, n_cols, max_state, allow_wrap):
        self.array = [[0 for x in range(n_rows)] for x in range(n_cols)]
        self.brray = [[0 for x in range(n_rows)] for x in range(n_cols)]
        self.use_array = True
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.max_state = max_state
        self.allow_wrap = allow_wrap

    def get_neighbour_states(self, x, y, size_of_neighbourHood):
        ret_list = []
        x_scan = []
        y_scan = []

        for off_set in range(size_of_neighbourHood + 1):
            x_scan.append(x - off_set)
            y_scan.append(y - off_set)

            if off_set != 0:
                x_scan.append(x + off_set)
                y_scan.append(y + off_set)

        for i in x_scan:
            for j in y_scan:
                # Ignore self
                if not (i == x and j == y):
                    # Decide what to do with cells off the grid
                    if i < 0 or i >= self.n_cols or j < 0 or j >= self.n_rows:
                        if self.allow_wrap:
                            # Convert the i and j values to wrap
                            if i < 0:
                                i = self.n_cols + i
                            elif i >= self.n_cols:
                                i = i - self.n_cols

                            if j < 0:
                                j = self.n_rows + j
                            elif j >= self.n_rows:
                                j = j -self.n_rows
                        else:
                            continue

                    if not self.use_array:
                        ret_list.append(self.brray[i][j])
                    else:
                        ret_list.append(self.array[i][j])

        return ret_list

    def get_state(self, x, y):
        x = int(x)
        y = int(y)
        if self.use_array:
            return self.array[x][y]
        else:
            return self.brray[x][y]

    def set_state(self, x, y, value):
        x = int(x)
        y = int(y)
        if self.use_array:
            self.array[x][y] = value
        else:
            self.brray[x][y] = value

    def increment_state(self, x, y):
        if self.get_state(x, y) != self.max_state:
            self.set_state(x, y, self.get_state(x, y) + 1)

    def decrement_state(self, x, y):
        if self.get_state(x, y) != 0:
            self.set_state(x, y, self.get_state(x, y) - 1)

    def apply_rule(self, rule):
        for i in range(self.n_cols):
            for j in range(self.n_rows):
                # Assume for now the neighbourhood size is 1
                if not self.use_array:
                    self.array[i][j] = rule(self.brray[i][j],  self.get_neighbour_states(i, j, 1))
                else:
                    self.brray[i][j] = rule(self.array[i][j], self.get_neighbour_states(i, j, 1))

        self.use_array = not self.use_array
