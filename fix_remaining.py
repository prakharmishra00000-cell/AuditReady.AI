import os

def fix_remaining(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    
    original = len(content)
    
    # Fix the comment line box-drawing chars (─)
    # Pattern: \xc3\x83\xc2\xa2"\xc3\xa2\xe2\x80\x9a\xc2\xac  (which is double-mojibake of ─)
    garbled_dash = b'\xc3\x83\xc2\xa2\"\xc3\xa2\xe2\x80\x9a\xc2\xac'
    count = content.count(garbled_dash)
    if count:
        print(f"  Replacing {count}x garbled dash in {filepath}")
        content = content.replace(garbled_dash, b'\xe2\x94\x80')
    
    # Also fix remaining support button sent text if still garbled
    garbled_sent = b'\xc3\x83\xc2\xa2\xc3\x85\xe2\x80\x9c... Query Sent'
    if garbled_sent in content:
        content = content.replace(garbled_sent, b'\xe2\x9c\x93 Query Sent')
        print(f"  Fixed Query Sent text in {filepath}")

    # Fix "→ Cloudflare" in comment
    cf_garbled = b'\xc3\x83\xc2\xa2\xc3\xa2\xe2\x80\xa0\xe2\x80\x99\''
    if cf_garbled in content:
        content = content.replace(cf_garbled, b'\xe2\x86\x92')
        print(f"  Fixed Cloudflare arrow in {filepath}")
    
    with open(filepath, 'wb') as f:
        f.write(content)
    print(f"  {filepath}: {original} -> {len(content)} bytes")

fix_remaining('index.js')
fix_remaining('admin/admin.js')
print("All done!")
