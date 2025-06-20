import boto3
import time
from botocore.exceptions import ClientError

def wait_for_localstack():
    """Wait for LocalStack to be fully ready"""
    print("Waiting for LocalStack to be ready...")
    time.sleep(5)  # Give LocalStack time to start properly

def setup_localstack_resources():
    """Setup all required LocalStack resources"""
    
    wait_for_localstack()
    
    # Initialize clients for LocalStack
    dynamodb_client = boto3.client(
        'dynamodb',
        endpoint_url='http://localhost:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
    
    dynamodb_resource = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

    # Check existing tables first
    def check_existing_tables():
        try:
            response = dynamodb_client.list_tables()
            existing_tables = response.get('TableNames', [])
            print(f"📋 Existing tables: {existing_tables}")
            return existing_tables
        except Exception as e:
            print(f"❌ Error checking tables: {e}")
            return []

    # Check existing buckets
    def check_existing_buckets():
        try:
            response = s3_client.list_buckets()
            existing_buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
            print(f"📋 Existing buckets: {existing_buckets}")
            return existing_buckets
        except Exception as e:
            print(f"❌ Error checking buckets: {e}")
            return []

    def create_table_if_not_exists(table_name, key_schema, attribute_definitions):
        """Create table only if it doesn't exist"""
        existing_tables = check_existing_tables()
        
        if table_name in existing_tables:
            print(f"⚠️  Table {table_name} already exists, skipping creation")
            return
        
        try:
            table = dynamodb_resource.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Wait for table to be created
            print(f"⏳ Creating table {table_name}...")
            table.wait_until_exists()
            print(f"✅ Created {table_name} table successfully")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f"⚠️  Table {table_name} already exists")
            else:
                print(f"❌ Error creating {table_name}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error creating {table_name}: {e}")

    def create_bucket_if_not_exists(bucket_name):
        """Create bucket only if it doesn't exist"""
        existing_buckets = check_existing_buckets()
        
        if bucket_name in existing_buckets:
            print(f"⚠️  Bucket {bucket_name} already exists, skipping creation")
            return
            
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"✅ Created {bucket_name} bucket successfully")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                print(f"⚠️  Bucket {bucket_name} already exists")
            else:
                print(f"❌ Error creating bucket {bucket_name}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error creating bucket {bucket_name}: {e}")

    print("🚀 Setting up LocalStack resources...")
    
    # Create DynamoDB Tables
    print("\n📊 Creating DynamoDB tables...")
    
    # PDF_Metadata table
    create_table_if_not_exists(
        'PDF_Metadata',
        [{'AttributeName': 'file_id', 'KeyType': 'HASH'}],
        [{'AttributeName': 'file_id', 'AttributeType': 'S'}]
    )
    
    # LLM_Metrics table
    create_table_if_not_exists(
        'LLM_Metrics',
        [{'AttributeName': 'run_id', 'KeyType': 'HASH'}],
        [{'AttributeName': 'run_id', 'AttributeType': 'S'}]
    )
    
    # QueryLog table
    create_table_if_not_exists(
        'QueryLog',
        [{'AttributeName': 'run_id', 'KeyType': 'HASH'}],
        [{'AttributeName': 'run_id', 'AttributeType': 'S'}]
    )

    # Create S3 Buckets
    print("\n🪣 Creating S3 buckets...")
    create_bucket_if_not_exists('pdf-storage-local')

    # Final verification
    print("\n🔍 Final verification...")
    final_tables = check_existing_tables()
    final_buckets = check_existing_buckets()
    
    print(f"\n✅ Setup complete!")
    print(f"📋 Tables created: {final_tables}")
    print(f"🪣 Buckets created: {final_buckets}")

if __name__ == "__main__":
    setup_localstack_resources()