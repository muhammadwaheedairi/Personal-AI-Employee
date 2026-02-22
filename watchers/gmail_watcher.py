"""Gmail watcher - monitors Gmail for important emails"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher
from config import Config

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(
            vault_path=Config.VAULT_PATH,
            check_interval=Config.CHECK_INTERVAL
        )
        self.credentials_path = Config.GMAIL_CREDENTIALS_PATH
        self.token_path = Path('token.pickle')
        self.service = self._authenticate()
        self.processed_ids = self._load_processed_ids()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        return build('gmail', 'v1', credentials=creds)
    
    def _load_processed_ids(self) -> set:
        """Load set of already processed email IDs"""
        processed_file = self.logs / 'processed_emails.txt'
        if processed_file.exists():
            return set(processed_file.read_text().splitlines())
        return set()
    
    def _save_processed_id(self, email_id: str):
        """Save processed email ID to avoid reprocessing"""
        processed_file = self.logs / 'processed_emails.txt'
        with open(processed_file, 'a') as f:
            f.write(f'{email_id}\n')
        self.processed_ids.add(email_id)
    
    def check_for_updates(self) -> list:
        """Check Gmail for unread starred emails"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:starred',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            
            # Filter out already processed
            new_messages = [
                m for m in messages 
                if m['id'] not in self.processed_ids
            ]
            
            return new_messages
            
        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
            return []
    
    def create_action_file(self, message) -> Path:
        """Create markdown file for email in Needs_Action folder"""
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()
            
            # Extract headers
            headers = {
                h['name']: h['value'] 
                for h in msg['payload']['headers']
            }
            
            from_email = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', datetime.now().isoformat())
            
            # Determine priority based on keywords in subject AND body
            snippet = msg.get('snippet', '').lower()
            subject_lower = subject.lower()
            priority_keywords = ['urgent', 'asap', 'important', 'deadline', 'critical']
            priority = 'high' if any(kw in snippet or kw in subject_lower for kw in priority_keywords) else 'medium'
            
            # Create markdown content with YAML frontmatter
            content = f"""---
type: email
source: gmail
from: {from_email}
subject: {subject}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
email_id: {message['id']}
---

# Email: {subject}

**From:** {from_email}  
**Date:** {date}  
**Priority:** {priority}

## Content Preview
{msg.get('snippet', 'No preview available')}

## Suggested Actions
- [ ] Read full email
- [ ] Draft reply
- [ ] Forward to relevant party
- [ ] Archive after processing

## Notes
<!-- Add your notes here -->

---
*Created by Gmail Watcher*
"""
            
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_subject = ''.join(c for c in subject if c.isalnum() or c in (' ', '-', '_'))[:50]
            filename = f'EMAIL_{timestamp}_{safe_subject}.md'
            filepath = self.needs_action / filename
            
            # Write file
            filepath.write_text(content)
            
            # Mark as processed
            self._save_processed_id(message['id'])
            
            return filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            raise

if __name__ == '__main__':
    watcher = GmailWatcher()
    watcher.run()