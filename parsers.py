import re


class BaseParser(object):
    def __init__(self, input):
        self.input = input

    def parse(self):
        return self.input


class IperfParser(BaseParser):
    def __init__(self, input):
        return super().__init__(input)
        self.parametres = ['Interval', 'Transfer', 'Bandwidth']
        self.template = (r'(?P<first>\S+-\s*\S+ \w+)\s*'
                         r'(?P<second>\S+ \w+)\s*'
                         r'(?P<third>\S+ \w+/\w+)')
                

    def parse(self):
        data = re.compile(self.template)
        matched_data = re.findall(data, self.string)
        j = 1
        for single_match in matched_data:
            i = 0
            dict_to_insert = dict()
            for name in self.column_names:
                dict_to_insert[name] = single_match[i]
                i += 1
            if j < len(matched_data)-1:
                interval_key = "Interval {}: {}".format(j, single_match[0])
            else:
                interval_key = "Average value:"
            j += 1
            self.output_dict[interval_key] = dict_to_insert
        return self.output_dict