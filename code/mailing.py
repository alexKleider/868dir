#!/usr/bin/env python3

# File: code/mailing.py

print("running code/mailing.py")

sender = "868directory@gmail.com"
recipients = ""
email_body = ""

emails = [ ]

email = {
    'From': sender,       # Mandatory field.
#   'Sender': sender,     # 0 or 1
#   'Reply-To': sender,   # 0 or 1
    'To': recipients,  # 1 or more, ',' separated
    'Cc': '',             # O or more comma separated
    'Bcc': '',            # O or more comma separated
    'Subject': subject,   # 0 or 1
    'attachments': [],
    'body': email_body,
}

if emails:
    helpers.dump2json_file(holder.emails,
            holder.email_json)
    n = len(holder.emails)
    efile = holder.email_json
    print(f"{n} emails sent to {efile}.")
    print(f"Emails ({len(holder.emails)} in " +
        f"number) sent to {holder.email_json}")
else:
    print("No emails to send.")

