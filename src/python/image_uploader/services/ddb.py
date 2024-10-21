import boto3
import os

from boto3.dynamodb.conditions import Key, Attr

from image_uploader.commons import constants
from image_uploader.commons.logger import logger
from image_uploader.models import DBModel

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb',
                          region_name=constants.REGION)


# Replace with your table name
def get_table(table_name):
    logger.info(f"Loading DDB table connection for {table_name}")
    table = dynamodb.Table(table_name)
    return table


def create_item(item: DBModel):
    table = get_table(item.table_name)
    print(item.__dict__)
    table.put_item(Item=item.__dict__)


def get_item(item: DBModel):
    table = get_table(item.table_name)
    response = table.get_item(Key=item.__dict__)
    item = response.get('Item')
    return item


def delete_item(item: DBModel):
    table = get_table(item.table_name)
    table.delete_item(Key=item.__dict__)


def get_item_by_pk(item: DBModel):
    table = get_table(item.table_name)
    item = table.query(
        KeyConditionExpression=Key(item.partition_key()).eq(item.__dict__[item.partition_key()])
    )
    return item


def get_items_by_gsi_contains(table_name, gsi, gsi_attr, value):
    table = get_table(table_name)
    items = []
    try:
        response = table.scan(
            IndexName=gsi,
            FilterExpression=Attr(gsi_attr).contains(value)
        )
        items = response.get('Items')
    except Exception as e:
        logger.error(e)
    return items


def get_items(table_name):
    table = get_table(table_name)
    response = table.scan(
        Limit=10
    )
    items = response.get('Items', [])
    return items
