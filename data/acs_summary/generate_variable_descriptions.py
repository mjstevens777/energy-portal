import csv
import json

templateFilePattern = "acs_summary/templates/csv/Seq%d.csv"

topics = []
topicLookup = {}
class Topic(object):
    def __init__(self, id):
        self.id = id
        self.tableGroups = []

    @staticmethod
    def create(id):
        if id not in topicLookup:
            topic = Topic(id)
            topicLookup[id] = topic
            topics.append(topic)
        return topicLookup[id]

    def addGroup(self, newGroup):
        for group in self.tableGroups:
            if group.id == newGroup.id:
                return
        self.tableGroups.append(newGroup)

    def flatten(self):
        return {
            "id": self.id,
            "groups": [group.id for group in self.tableGroups]
        }

tableGroups = []
tableGroupLookup = {}
class TableGroup(object):
    def __init__(self, id):
        self.id = id
        self.tables = []

    @staticmethod
    def create(id):
        if id not in tableGroupLookup:
            group = TableGroup(id)
            tableGroupLookup[id] = group
            tableGroups.append(group)
        return tableGroupLookup[id]

    def addTable(self, newTable):
        for table in self.tables:
            if table.id == newTable.id:
                return
        self.tables.append(newTable)

    def flatten(self):
        return {
            "id": self.id,
            "tables": [table.id for table in self.tables]
        }

tables = []
tableLookup = {}
class Table(object):
    def __init__(self, row):
        self.id = row["Table Number"]
        self.topic_id = self.id[:3]
        self.group_id = self.id[:6]
        self.description = row["Table Title"]
        self.restrictions = row["Geography Restrictions"]
        if self.restrictions == "":
            self.restrictions = None
        sequence = row["Summary File Sequence Number"]
        self.sequences = [sequence]
        startend = row["Summary File Starting and Ending Positions"]
        start, end = startend.split("-")
        start, end = int(start), int(end)
        self.locations = [(sequence, start, end)]
        self.size = end - start + 1
        self.variables = []

    @staticmethod
    def create(*args, **kwargs):
        table = Table(*args, **kwargs)
        topic = Topic.create(table.topic_id)
        group = TableGroup.create(table.group_id)
        topic.addGroup(group)

        if table.id in tableLookup:
            tableLookup[table.id].merge(table)
        else:
            tableLookup[table.id] = table
            tables.append(table)
        table = tableLookup[table.id]
        group.addTable(table)
        return table

    def merge(self, other):
        self.size += other.size
        self.locations += other.sequences
        self.sequences += other.sequences

    def addVariable(self, variable):
        self.variables.append(variable)

    def flatten(self):
        if len(self.variables) != self.size:
            print(self.id)
            print(len(self.variables))
            print(self.size)
            raise Exception("Missing variable")
        data = {
            "variables": [var.id for var in self.variables]
        }
        for key in ["id", "description", "restrictions",
                    "sequences", "locations", "size"]:
            data[key] = getattr(self, key)
        return data

variables = []
variableLookup = {}
class Variable(object):
    def __init__(self, id, description, sequence, position):
        self.id  = id
        self.description = description
        self.sequence = sequence
        self.position = position
        self.tableId = self.id.split("_")[0]


    @staticmethod
    def create(*args, **kwargs):
        variable = Variable(*args, **kwargs)
        if variable.id not in variableLookup:
            variables.append(variable)
            variableLookup[variable.id] = variable
        return variable

    def flatten(self):
        return {
            "id": self.id,
            "description": self.description,
            "sequence": self.sequence,
            "position": self.position
        }

with open("acs_summary/tables.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        Table.create(row)

varnames = []
vardescriptions = {}
for i in range(121):
    sequence = "%04d" % (i + 1)
    file_name = templateFilePattern % (i + 1)
    with open(file_name) as f:
        seqvarnames = f.readline().strip().split(",")[6:]
        varnames += seqvarnames
        f.seek(0)
        reader = csv.DictReader(f)
        for row in reader:
            for i, name in enumerate(seqvarnames):
                var = Variable.create(name, row[name], sequence, i + 6)
                tableLookup[var.tableId].addVariable(var)
            break


data = {
    "topics": dict(((topic.id, topic.flatten()) for topic in topics)),
    "groups": dict(((group.id, group.flatten()) for group in tableGroups)),
    "tables": dict(((table.id, table.flatten()) for table in tables)),
    "variables": dict(((var.id, var.flatten()) for var in variables)),
    "topicIds": [topic.id for topic in topics],
    "groupIds": [group.id for group in tableGroups],
    "tableIds": [table.id for table in tables],
    "variableIds": [var.id for var in variables]
}

with open("acs_summary/variables.json", "w") as f:
    json.dump(data, f, indent=2, sort_keys=True)
