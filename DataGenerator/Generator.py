import re
import functions_and_their_mappings
import configparser

schema_dictionary = dict()
tables_discovered_so_far = []
output_path = ""
config_file_path = "../config/configurations.ini"
output_path = "../output/"


def column_parser(column):
    column_name = column
    variable_length = column.find('(')
    if variable_length != -1:
        column_name = column[: variable_length]
        max_length_of_column_data = column[variable_length + 1: -1]
        if column_name == "DECIMAL" or column_name == "NUMERIC":
            index_of_comma = max_length_of_column_data.find(',')
            min_length = int(max_length_of_column_data[: index_of_comma])
            max_length = int(max_length_of_column_data[index_of_comma + 1:])
            return functions_and_their_mappings.two_arguments_functions[column_name](min_length, max_length)
        else:
            max_length_of_column_data = int(max_length_of_column_data)
            return functions_and_their_mappings.one_argument_functions[column_name](max_length_of_column_data)
    else:
        return functions_and_their_mappings.no_argument_functions[column_name]()


def generate_table_data (table_key_and_columns_in_array, number_of_records):
    string_to_be_written = ""
    table_name = table_key_and_columns_in_array[0]
    columns_in_table = table_key_and_columns_in_array[1]
    for k in range(number_of_records):
        for i in columns_in_table[: -1]:
            string_to_be_written += str(column_parser(i)) + ","
        string_to_be_written += str(column_parser(columns_in_table[-1])) + "\n"
    with open(output_path + table_name + ".csv", "a") as f:
        f.write(string_to_be_written)
        print("Done writing file: " + table_name)


def data_generator(ddl_file_path, number_of_records):
    parse_schema_ddl(ddl_file_path)
    for each_item in schema_dictionary.items():
        generate_table_data(each_item, number_of_records)


def attribute_extractor_regex_for_redshift_schema(line):
    global schema_dictionary
    global tables_discovered_so_far
    attribute = re.search(r'\s*\w+\s+((?:SMALLINT)|(?:INT2)|(?:INTEGER)|(?:INT)|(?:INT4)|(?:BIGINT)|(?:INT8)|(?:DECIMAL\(.*\))|(?:NUMERIC\(.*\))|(?:REAL)|(?:FLOAT4)|(?:DOUBLE\s+PRECISION)|(?:FLOAT8)|(?:FLOAT)|(?:BOOLEAN)|(?:BOOL)|(?:CHAR(?:\(.*\))?)|(?:CHARACTER(?:\(.*\))?)|(?:NCHAR(?:\(.*\))?)|(?:BPCHAR(?:\(.*\))?)|(?:VARCHAR\(.*\))|(?:CHARACTER\s+VARYING\(.*\))|(?:NVARCHAR\(.*\))|(?:TEXT\(.*\))|(?:DATE)|(?:DATETIME)|(?:TIMESTAMP)|(?:TIMESTAMP\s+WITHOUT\s+TIME\s+ZONE)|(?:TIMESTAMPTZ)|(?:TIMESTAMP\s+WITH\s+TIME\s+ZONE))(\(\d+(,\d+)?\))?\s?(?:NOT)?\s?(?:NULL)?\s?(?:ENCODE\s\w+)?,?', line)
    if attribute:
        column_type = attribute.group(1)
        latest_table = tables_discovered_so_far[-1]
        schema_dictionary.setdefault(latest_table, []).append(column_type)
        return attribute


def regex_identifier_for_new_table(line):
    global tables_discovered_so_far
    new_table = re.search(r'\s*CREATE\s+TABLE\s+(?:IF\s*NOT\s+EXISTS\s+)?(.*)\s*', line)
    if new_table:
        new_table_name = new_table.group(1).rstrip()
        tables_discovered_so_far.append(new_table_name)


def parse_schema_ddl(file_path):
    with open(file_path, 'r') as schema:
        schema_as_a_string = schema.read()

    for line in schema_as_a_string.splitlines():
        line = line.upper()
        regex_identifier_for_new_table(line)
        attribute_extractor_regex_for_redshift_schema(line)


config = configparser.ConfigParser()
config.read(config_file_path)
schema_file_path = config.get('SETTINGS', 'FilePath')
number_of_records_to_insert = int(config.get('SETTINGS', 'NumberOfRecords'))
data_generator(schema_file_path, number_of_records_to_insert)