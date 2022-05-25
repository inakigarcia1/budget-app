import math
class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def get_withdraws(self):
        withdraw = 0
        for movement in self.ledger:
            if "Transfer" not in movement['description']:
                if movement['amount'] < 0:
                    withdraw += movement['amount']

        return withdraw * -1

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if not self.check_funds(amount):
            return False

        self.ledger.append({'amount': -amount, 'description': description})
        return True

    def get_balance(self):
        total = 0
        for dict in self.ledger:
            total += dict['amount']

        return total

    def transfer(self, amount, category):
        if not self.check_funds(amount):
            return False

        category.ledger.append({'amount': amount, 'description': f'Transfer from {self.name}'})
        self.ledger.append({'amount': -amount, 'description': f'Transfer to {category.name}'})
        return True

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False

        return True

    def __repr__(self):
        line1 = f"{self.name.center(30, '*')}\n"
        lines = ''
        for movement in self.ledger:
            desc = movement['description']
            if len(movement['description']) > 23:
                cDesc = ''
                for i in range(23):
                    cDesc += desc[i]
                desc = cDesc

            amount = movement['amount']

            if len(str(amount)) > 7:
                if type(amount) == "float":
                    amount = round(amount)
                cMount = ''
                strMount = str(amount)
                for i in range(4):
                    cMount += strMount[i]
                amount = cMount

            amount = float(amount)
            amount = "%.2f" % amount

            lDesc = len(desc)
            lAmount = len(str(amount))

            space = 30 - lDesc
            space = space - lAmount
            amount = amount.rjust(space + lAmount, ' ')

            lines += f'{desc}{amount}\n'

        line3 = f'Total: {self.get_balance()}'

        return line1 + lines + line3


def create_spend_chart(categories):
    total_withdraw = 0
    withdraws = []
    for category in categories:
        total_withdraw += category.get_withdraws()
        withdraws.append({'name': category.name, 'withdraw': category.get_withdraws()})

    # print(total_withdraw)

    for withdraw in withdraws:
        actual = withdraw['withdraw']
        # print(actual)
        percentage = (actual * 100) / total_withdraw
        # print(percentage)
        if percentage < 10:
          percentage = 1
        percentage = round(percentage / 10) * 10
        withdraw['withdraw'] = percentage

    # print(withdraws)

    spaces = 3 * len(categories)
    j = 100
    graph = ''
    dot_line = ''
    for n in range(11):
        points = 0
        location = []
        line = f'{j}|'
        for withdraw in withdraws:
            if j == withdraw['withdraw']:
                points += 1
                location.append(withdraws.index(withdraw))

        line = line.rjust(4, ' ')

        ph = False
        if dot_line != '':
            if points != 0:
                if len(location) == 1 and 0 in location:
                    line += ' '
                    line += 'o'
                    ph = True
            k = 0
            for char in dot_line:
                if ph:
                    if k < 6:
                        k += 1
                        continue
                    if char == 'o':
                        line += 'o'
                        continue
                    line += ' '
                else:
                    if k < 4:
                        k += 1
                        continue
                    if char == 'o':
                        line += 'o'
                        continue
                    line += ' '

        # print(points)
        # print(location)
        if points != 0:
            if dot_line != '':
                for i in range(1, max(location) + 1):
                    line += ' '
                    if i in location:
                        line += 'o'
                dot_line = line
            else:
                if 0 in location:
                    line += ' o'
                else:
                    line += '  '

                for i in range(1, max(location) + 1):
                    line += '  '
                    if i in location:
                        line += 'o'
                dot_line = line


        limit = spaces + 1
        limit += 4
        add = limit - len(line)
        # print(add)
        for i in range(add):
            line += ' '
        graph += f'{line}\n'
        j -= 10
        # print(location)

    dashes = ''
    for i in range(spaces + 1):
        dashes += '-'
    dashes = dashes.rjust(4 + len(dashes), ' ')
    graph += dashes

    largest = ''
    for category in categories:
        if len(category.name) > len(largest):
            largest = category.name

    title = 'Percentage spent by category\n'
    names = '     '
    skips = []
    for i in range(len(largest)):
        c = 0
        for category in categories:
            if category.name in skips:
                if c == 3:
                    names += '  \n'
                else:
                    names += '   '
                c += 1
                continue

            if i < len(category.name):
                if i + 1 == len(largest):
                  names += f'{category.name[i]}  '
                else:
                  names += f'{category.name[i]}'
                  c += 1
                  if c == 3:
                      names += '  \n     '
                  else:
                      names += '  '
            else:
                skips.append(category.name)
                if c == 3:
                    names += '  \n'
                else:
                    names += '   '
                c += 1

    return f'{title}{graph}\n{names}'
