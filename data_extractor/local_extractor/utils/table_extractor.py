import boto3
import json
import pathlib
import os


class TexTract(object):

    def __init__(self):

        self._parentdir = pathlib.Path(__file__).parent.absolute()
        self.api_fpath = os.path.join(self._parentdir, "api_keys", "aws.json")
        self.service_name = 'textract'
        self.region_name = 'us-west-2'
        self.access_key = None
        self.secret_access_key = None

        self.__read_api_key__()


    def __read_api_key__(self):

        with open(self.api_fpath, 'r') as f:
            api_data = json.load(f)
        
        self.access_key = api_data['ACCESS_KEYID']
        self.secret_access_key = api_data['SECRET_ACCESS_KEY']

    def _get_rows_columns_map_(self, table_result, blocks_map):
        
        rows = {}
        for relationship in table_result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            # create new row
                            rows[row_index] = {}
                            
                        # get the text value
                        rows[row_index][col_index] = self._get_text_(cell, blocks_map)
        return rows


    def _get_text_(self, result, blocks_map):
        text = ''
        if 'Relationships' in result:
            for relationship in result['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
                        if word['BlockType'] == 'SELECTION_ELEMENT':
                            if word['SelectionStatus'] =='SELECTED':
                                text +=  'X '    
        return text
    
    def _generate_table_csv_(self, table_result, blocks_map, table_index):
        rows = self._get_rows_columns_map_(table_result, blocks_map)
        
        # get cells.
        csv = ''

        for row_index, cols in rows.items():
            
            for col_index, text in cols.items():
                csv += '{}'.format(text) + ","
            csv += '\n'
            
        csv += '\n\n\n'
        return csv


    def _generate_table_list_(self, table_result, blocks_map):
        rows = self._get_rows_columns_map_(table_result, blocks_map)
        
        # get cells.
        data = []

        for row_index, cols in rows.items():
            datarow = []
            for col_index, text in cols.items():
                datarow.append(text)
            data.append(datarow)
            
        return data


    def get_table_from_img(self, imgdata):

        client = boto3.client(
            self.service_name, region_name=self.region_name, 
            aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_access_key)

        response = client.analyze_document(Document={'Bytes': imgdata}, FeatureTypes=['TABLES'])

        blocks=response['Blocks']

        blocks_map = {}
        table_blocks = []

        for block in blocks:
            blocks_map[block['Id']] = block
            if block['BlockType'] == "TABLE":
                table_blocks.append(block)

        if len(table_blocks) <= 0:
            return None

        tables = {}
        for index, table in enumerate(table_blocks):
            tables[index] = self._generate_table_list_(table, blocks_map)

        return tables
