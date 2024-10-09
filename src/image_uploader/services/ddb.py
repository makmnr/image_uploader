import boto3
import os

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb',
                          region_name=os.getenv('AWS_REGION'))

# Replace with your table name
table_name = 'YourTableName'  # Change this to your DynamoDB table name
table = dynamodb.Table(table_name)


def create_item(model):
    """Save a Pydantic model instance to DynamoDB."""
    table.put_item(Item=model.dict())


def get_item(primary_key: dict):
    """Retrieve an item from DynamoDB and return it as a Pydantic model instance."""
    response = table.get_item(Key=primary_key)
    item = response.get('Item')
    return item


def delete_item(primary_key: dict):
    """Delete an item from DynamoDB using the primary key."""
    table.delete_item(Key=primary_key)


# TODO
def list_items(filters=None):
    """List items in the table, applying optional filters, and return them as Pydantic model instances."""
    response = table.scan()
    items = response.get('Items', [])

    return items
