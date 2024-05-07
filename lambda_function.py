import boto3
import csv

# Initializing the boto3 client
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

def lambda_handler(event, context):
    # Assigning bucket name
    bucket_name = 'inbooster' 

    try:
        # Retrieving the CSV file from S3
        csv_file = s3_client.get_object(Bucket=bucket_name, Key='contacts.csv')
        # Formatting the entries
        lines = csv_file['Body'].read().decode('utf-8').splitlines()
        
        # Retrieving the HTML email template from S3
        email_template = s3_client.get_object(Bucket=bucket_name, Key='template.html')
        # Formatting the template
        email_html = email_template['Body'].read().decode('utf-8')
        
        # Parsing the CSV file
        contacts = csv.DictReader(lines)
        
        for contact in contacts:
            
            # Replacing placeholders in the email template with contact information
            personalized_email = email_html.replace('{{FirstName}}', contact['FirstName'])
            
            # Sending the email using SES
            response = ses_client.send_email(
                
                # Sender
                Source='shahanashanmugaraja20@gmail.com', 
                
                # Receivers
                Destination={'ToAddresses': [contact['Email']]},
                Message={
                    'Subject': {'Data': 'Sale on Online Courses', 'Charset': 'UTF-8'},
                    'Body': {'Html': {'Data': personalized_email, 'Charset': 'UTF-8'}}
                }
            )
            print(f"Email sent to {contact['Email']}: Response {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
