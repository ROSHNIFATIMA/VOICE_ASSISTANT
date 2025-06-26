import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def get_gmail_service():
    """Gets an authorized Gmail API service instance."""
    creds = None
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        raise FileNotFoundError(
            "credentials.json file not found! "
            "Please download it from Google Cloud Console and place it in the project directory."
        )
    
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            print("Successfully loaded existing credentials from token.pickle")
        except Exception as e:
            print(f"Error loading token.pickle: {e}")
            print("Will create new credentials...")
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing expired credentials...")
                creds.refresh(Request())
                print("Credentials refreshed successfully!")
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                print("Will create new credentials...")
                creds = None
        
        if not creds:
            try:
                print("Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("OAuth flow completed successfully!")
            except Exception as e:
                print(f"Error during OAuth flow: {e}")
                raise
        
        # Save the credentials for the next run
        try:
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            print("Credentials saved to token.pickle")
        except Exception as e:
            print(f"Error saving credentials: {e}")

    try:
        service = build('gmail', 'v1', credentials=creds)
        print("Gmail service built successfully!")
        return service
    except Exception as e:
        print(f"Error building Gmail service: {e}")
        raise

def send_email(service, to, subject=None, body=None):
    """Send an email using Gmail API."""
    try:
        # Get sender email from environment variable
        sender_email = os.getenv('SENDER_EMAIL')
        if not sender_email:
            print("Error: SENDER_EMAIL not found in environment variables")
            return False

        # Use default subject if none provided
        if not subject:
            subject = os.getenv('DEFAULT_SUBJECT', 'msg from vc assistant')

        # Create message
        message = {
            'raw': create_message(sender_email, to, subject, body or '')
        }
        
        print(f"Attempting to send email to: {to}")
        print(f"From: {sender_email}")
        print(f"Subject: {subject}")
        
        sent_message = service.users().messages().send(
            userId='me', body=message).execute()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def create_message(sender, to, subject, body):
    """Create a message for an email."""
    import base64
    from email.mime.text import MIMEText
    
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return raw.decode()

def read_emails(service, max_results=5):
    """Read the latest emails from Gmail."""
    try:
        print(f"Fetching latest {max_results} emails...")
        results = service.users().messages().list(
            userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No messages found in inbox")
            return []
        
        print(f"Found {len(messages)} messages")
        email_list = []
        for message in messages:
            try:
                msg = service.users().messages().get(
                    userId='me', id=message['id']).execute()
                
                headers = msg['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                sender = next(h['value'] for h in headers if h['name'] == 'From')
                
                # Get email body
                if 'parts' in msg['payload']:
                    parts = msg['payload']['parts']
                    data = parts[0]['body'].get('data', '')
                else:
                    data = msg['payload']['body'].get('data', '')
                
                if data:
                    import base64
                    content = base64.urlsafe_b64decode(data).decode()
                else:
                    content = "No content"
                
                email_list.append({
                    'subject': subject,
                    'sender': sender,
                    'content': content[:200] + "..." if len(content) > 200 else content
                })
            except Exception as e:
                print(f"Error processing message {message['id']}: {e}")
                continue
        
        return email_list
    except Exception as e:
        print(f"Error reading emails: {e}")
        return [] 