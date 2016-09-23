import json, csv


class ConfigMap(object):
    "Class to handle djangos __getattr__"
    conf_width = []#Keep track of the maximum text size for that column 
    def __init__(self, value, config, index):
        value = value.strip()
        self.value = value
        while (len(self.conf_width) <= index):
            self.conf_width.append(0)
        self.conf_width[index] = max(len(value), self.conf_width[index])
        self._type = config.get("validation", {}).get("fieldType", "string")
        self.size =config.get("validation", {}).get("fieldSize", None)
        self.valid = True #Valid by default
        if self._type == "string":
            if self.size:
                self.valid = (len(value) <= self.size)
        if self._type == "integer":
            try:
                int(value)
            except:
                self.valid = False
        self.style = ['style="color:red; "', 'style="color:blue; "'][self.valid]
        self.type = ['type="text"', 'type="number"'][ self._type == 'integer' ]
    def __getitem__(self, value):
        return self.__getattr__(value)
    @classmethod
    def close(cls):
        _sum = float(sum(cls.conf_width))
        cls.conf_width = [(120 * x/_sum) for x in cls.conf_width]
        



def test_headers(headers, config):
    """
    This function tests whether all the input csv file's
    headers are mapped in the  config file.
    If a header is not found in the config file, the header name is returned,
    otherwise, it returns a dict mapping the 
    """
    headers2 = [h.replace("*", "") for h in headers]#Resolve the instances when the "ContactName" header appears as "*ContactName"
    mapping = {} #This holds a mapping of the form: {'html_table_header': csv_row_index }
    for header in config["headers"]:
        if header in headers:
            mapping[header] = headers.index(header)
        elif header in headers2:
            mapping[header] = headers2.index(header)
        else:
            return header
    return mapping



def csv_process(fl, config, row_id):
    """
    process CSV data, return the data as row-major matrix of data
    :type output: list(list(str))
    return output, row_id
    """
    file_obj = fl
    try:
        csv_file = csv.reader(file_obj)
    except:
        return None, "Error reading/parsing the csv file. Is it well formed?"
    first_line = True
    output = [] #Major matrix list of csv data
    for row in csv_file:
        if first_line:
            first_line = False
            header_rows = row
            mapping = test_headers(header_rows, config)
            if type(mapping) != dict:#The sourceHeader 'mapping' is missing from the headers of the csv files
                res = "The csv file doesn't contain a column header called <b>%s</b> from the configuration file. \n"\
                  "This is required for mapping of the header rows. Check the csv header spelling and ensure\n"\
                  "that you are using the correct configuration file!!" %mapping
                return None, res
            continue
        row2 = []
        index = 0
        for h, c in zip(config["headers"], config["fields"]):
            if h in mapping:
                row2.append(ConfigMap(row[mapping[h]], c, index))
            else:
                row2.append(ConfigMap("", c, index))
            index = index + 1
        output.append(row2)
        row_id += 1
    if not output:
        return None, "No output generated. Does the CSV file contain data?"
    return output, row_id


def parse_config_file(fp):
    try:
        config = json.loads(fp)
    except:
        return None
    if config.get("fields"):
        config["columns"] = len(config.get("fields")) #The expected number of columns
    else:
        config["columns"] = 0
    sourceFields = []#List of config's source fields headers.
    destFields = []
    for field in config["fields"]:
        sourceFields.append(field.get("sourceField", "")) # List of all the field headers expected from the input CSV files
        destFields.append(field.get("destField", "")) # List of all the field headers to be used in the output CSV/XML files
    config["headers"] = sourceFields
    config["dest_headers"] = destFields
    return config


def parse_data(config, cell_data, id):
    "return 'True' if 'cell_data' meets the requirements, else, return False"
    conf_len = False
    if config["fields"][id].get("validation") and config["fields"][id].get("validation", {}).get("fieldSize"):
        conf_len = int(config["fields"][id]["validation"]["fieldSize"] )
    if conf_len and len(cell_data) > conf_len:
        return False, None
    if config["fields"][id].get("validation") and config["fields"][id]["validation"].get("fieldType") == "integer":
        try:
            int(cell_data.strip())
            return True, int
        except:
            return False, int
    return True, None

def main(csv_files, config):
    table = []
    row_id = 0 #The id  if the next html row
    for fl in csv_files:
            csv_list, row_id = csv_process(fl, config, row_id)
            if  not csv_list: #an error occurred.
                return "Error while processing file: %s\n%s"%(fl.name, row_id)
            table.extend(csv_list)
    if not table:
        return None
    #ConfigMap.close()
    row_nmbr = 0
    for row in table: #Set the width of each column
        for item, width in zip(row, ConfigMap.conf_width):
            item.row_nmbr = row_nmbr
            item.cell_width = width
            row_nmbr += 1
    return table

