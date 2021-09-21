import csv

class QuerySetCSVExporter:

    def __init__(self, queryset, filename):
        self.queryset = queryset
        self.filename = filename

    def export(self):
        fields_dicts = self.queryset.values()
        if len(fields_dicts) == 0:
            return
        with open(self.filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(fields_dicts[0].keys())
            for fields_dict in fields_dicts:
                writer.writerow(fields_dict.values())
