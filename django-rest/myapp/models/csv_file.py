

class CsvFile(object):
    def __init__(self, filename):
        self.header = None
        self.data = None

        with open(filename) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        if len(content) > 0:
            header = content.pop(0).split(',')
            self.header = [x.strip() for x in header]
            self.data = []
            for row in content:
                r = row.split(',')
                self.data.append([x.strip() for x in r])

    def json(self):
        return {
            "header": self.header,
            "data": self.data,
        }

