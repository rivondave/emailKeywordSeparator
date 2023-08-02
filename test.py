import re
import asyncio
from validate_email import validate_email

def is_valid_email(email):
    is_valid = validate_email(email)
    return is_valid

def get_keyword(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    entries = [line.strip() for line in content if line.strip()]
    keyword_list = list(set(entries))
    duplicates = [entry for entry in entries if entries.count(entry) > 1]
    return keyword_list

def write_to_file(file_path, emails):
    with open(file_path, 'w') as file:
        file.write('\n'.join(emails))

async def filter_emails_with_keyword(email_file, keyword, invalid_file, matched, unmatched):

    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
    with open(email_file, 'r') as infile, open(invalid_file, 'w') as invalid, open(matched, 'w') as match, open(unmatched, 'w') as unmatch:
        while True:
            chunk = infile.readline(1024)  # Read in chunks of 1024 bytes
            if not chunk:
                break
            emails = email_pattern.findall(chunk)
            for email in emails:
                result = is_valid_email(email)
                if result:
                    if keyword.lower() in email.lower():
                        match.write(email + '\n')
                    else:
                        unmatch.write(email + '\n')
                else:
                    invalid.write(email + '\n')

async def main():
    email_file = input("Enter path to email file: ")
    keyword_file = input("Enter path to keyword file: ")

    matched = 'matched_emails.txt'
    unmatched = 'unmatched_emails.txt'
    invalid_emails = 'invalid_emails.txt'

    keyword_list = get_keyword(keyword_file)

    # for keyword in keyword_list:
    #     await filter_emails_with_keyword(email_file, keyword, invalid_emails, matched, unmatched)
    
    # print(keyword_list)
    keyword_length = len(keyword_list)

    count = 0
    while count < keyword_length:
        await filter_emails_with_keyword(email_file, keyword_list[count], invalid_emails, matched, unmatched)
        print(keyword_list[count])
        count = count+1
    print("Email classification done.....")
    

if __name__ == "__main__":
    asyncio.run(main())
