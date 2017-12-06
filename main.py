import sys


class Map(object):

    def __init__(self, input_file):
        f = open(input_file, 'r')
        lines = list(f)

        w, h = lines[0].strip().split(' ')
        self.width = int(w)
        self.height = int(h)

        x, y, direction = lines[1].strip().split(' ')
        self.player = (int(x), int(y))
        self.direction = direction

        self.tokens = {}
        self.travelled = set()

        for line in lines[2:]:
            line = line.strip()
            x, y, token = line.split(' ')
            self.tokens[x + ',' + y] = token

        print('Parsed file, player location: %s, laser direction: %s, tokens: %s' % (
            self.player, self.direction, self.tokens))

    def get_token(self, x, y):
        s = '%s,%s' % (x, y)
        return self.tokens.get(s)

    def print_board(self):
        s = ''
        for x in range(self.width):
            for y in range(self.height):
                token = self.get_token(x, y)
                if token:
                    s += token
                elif (x, y) == self.player:
                    s += self.direction
                else:
                    s += '.'
            s += '\n'
        print('')
        print(s)
        print('')

    def out_of_bounds(self, x, y):
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def state_str(self):
        return '%s,%s,%s' % (self.player[0], self.player[1], self.direction)

    def tick(self):
        # Figure out the next slot
        # If out of bounds, game ends
        # If we've already been there in that direction, game ends
        # Otherwise, remember that we've been there in that direction
        # And update the state

        deltas = {
            'S': (0, -1),
            'N': (0, 1),
            'E': (1, 0),
            'W': (-1, 0),
        }
        delta = deltas[self.direction]
        player_next = (self.player[0] + delta[0], self.player[1] + delta[1])

        state_str = self.state_str()
        if state_str in self.travelled:
            return True, (-1, None)

        self.travelled.add(state_str)

        if self.out_of_bounds(*player_next):
            return True, (len(self.travelled), self.player)

        transform = {
            '\\': {
                'S': 'E',
                'N': 'W',
                'E': 'S',
                'W': 'N',
            },
            '/': {
                'S': 'W',
                'N': 'E',
                'E': 'N',
                'W': 'S',
            },
        }
        token_next = self.get_token(*player_next)
        if not token_next:
            direction_next = self.direction
        else:
            direction_next = transform[token_next][self.direction]

        self.player = player_next
        self.direction = direction_next

        return False, None


if __name__ == '__main__':
    print(sys.argv)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    map = Map(input_file)
    map.print_board()

    i = 0
    done = False
    while not done:
        i += 1
        done, rval = map.tick()
        print('move %i, %s %s' % (i, done, rval))
        map.print_board()

    s = str(rval[0]) + '\n'
    if rval[1]:
        s += '%s %s\n' % (rval[1][0], rval[1][1])
    with open(output_file, 'w') as f:
        f.write(s)
