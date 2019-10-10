import os
import yaml
import json
from graphqlclient import GraphQLClient
#
# CONSTANTS
#
LBOX_PATH=os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH="{}/lbox.config.yaml".format(LBOX_PATH)
CREATE_DS_ERROR="lbox.api.create_dataset: connecting to projects not yet implemented"

#
# HELPERS
#
def config(*keys):
    """ load meta data yaml
    Args:
        *keys: series of keys to extract element of interest
    """
    cfig=yaml.safe_load(open(CONFIG_PATH))
    for key in keys:
        cfig=cfig[key]
    return cfig


#
# API
#
def get_client(client_url=None,api_key=None,cfig=None):
    if not (client_url and api_key):
        if not cfig:
            cfig=config()
        client_url=cfig['client']
        api_key=cfig['api_key']
    client=GraphQLClient(client_url)
    client.inject_token(f'Bearer {api_key}')
    return client


def get_ids(dataset_id,client=None):
    response_str=_client(client).execute(
        QUERY['get_ids'],
        {'dataSetId': dataset_id})
    response=json.loads(response_str)
    return [d['id'] for d in response['data']['dataset']['dataRows']]


def get_filtered_ids(dataset_id,external_ids,client=None):
    response_str=_client(client).execute(
        QUERY['get_ids'],
        {'dataSetId': dataset_id})
    response=json.loads(response_str)
    rows=response['data']['dataset']['dataRows']
    return [row['id'] for row in rows if row['externalId'] in external_ids]
    

def delete_datarows(datarow_ids,client=None):
    response_str=_client(client).execute(
        QUERY['delete_datarows'],
        {'datarowIds': datarow_ids})
    response=json.loads(response_str)
    return response['data']['deleteDataRows']


def bulk_import(dataset_id,url,client=None):
    response_str=_client(client).execute(
        QUERY['bulk_import'],
        {'dataSetId': dataset_id,'jsonURL': url})
    response=json.loads(response_str)
    return response['data']['appendRowsToDataset']['accepted']


def add_info(datarow_id,value=None,typ='TEXT',client=None):
    if not value: value=datarow_id
    response_str=_client(client).execute(
        QUERY['add_info'], 
        {'dataRowId': datarow_id,'metaValue': value,'metaType': typ})
    response=json.loads(response_str)
    return response['data']['createAssetMetadata']


def create_dataset(dataset_name,projects=None,project_ids=[],client=None):
    if projects or project_ids: 
        # projects={ 'connect': [pid for pid in project_ids] }
        raise NotImplementedError(CREATE_DS_ERROR)
    response_str=_client(client).execute(
        QUERY['create_dataset'], 
        {'dataSetName': dataset_name,'projects': projects})
    response=json.loads(response_str)
    return response['data']['createDataset']['id']


#
# INTERNAL
#
def _client(client):
    if not client:
        client=get_client()
    return client



#
# QUERIES
#
QUERY={
    "create_dataset": """
        mutation createDataset($dataSetName: String!){
          createDataset(
            data:{
              name: $dataSetName            
            }
          ) {
            id
          }
        }
    """,
    "bulk_import":"""
        mutation AppendRowsToDataset($dataSetId: ID!, $jsonURL: String!){
          appendRowsToDataset(
            data:{
              datasetId: $dataSetId,
              jsonFileUrl: $jsonURL,
            }
          ){
            accepted
          }
        } 
    """,
    "get_ids": """
        query getDataRowIds($dataSetId: ID!){
          dataset(where:{id:$dataSetId}){
            id
            dataRows(first:100, skip:0){
              id
              externalId
              rowData

            }
          }
        }
    """,
    "add_info": """
        mutation AddAssetInfo($dataRowId:ID!, $metaValue:String!, $metaType: MetadataType!) {
          createAssetMetadata(
            data: {
              dataRowId: $dataRowId,
              metaValue: $metaValue,
              metaType: $metaType,
            }
          ) {
            id
          }
        }
    """,
    "delete_datarows":"""
          mutation DeleteDataRowsFromAPI($datarowIds: [ID!]!) {
            deleteDataRows(where:{
              dataRowIds: $datarowIds
            }){
              id
              deleted
            }
          }
    """
}