import os

def fix_file(filepath, is_admin=False):
    with open(filepath, 'rb') as f:
        content = f.read()
    
    original_len = len(content)
    
    # All known garbled sequences in both files
    replacements = [
        # Arrow: Ã¢â†'' (mojibake for →)  - multiple variants
        (b'\xc3\x83\xc2\xa2\xc3\xa2\xe2\x80\xa0\xe2\x80\x99\'', b'\xe2\x86\x92'),  # → variant 1
        (b'\xc3\xa2\xe2\x80\xa0\xe2\x80\x99\'', b'\xe2\x86\x92'),   # → variant 2
        (b'\xc3\xa2\xe2\x80\xa0\xc2\x92', b'\xe2\x86\x92'),          # → variant 3
        
        # ⚠️ warning emoji
        (b'\xc3\xa2\xc5\xa1\xc2\xa0\xc3\xaf\xc2\xb8\xc2\x8f', b'\xe2\x9a\xa0\xef\xb8\x8f'),
        
        # ⚠ warning triangle (in Issues Found)
        (b'\xc3\x83\xc2\xa2\xc3\x85\xc2\xa1\xc3\x82\xc2\xa0\xc3\x83\xc2\xaf', b'\xe2\x9a\xa0'),
        
        # ✓ checkmark (... Clean, ... Query Sent, ... Scan complete, ... Manual Scan)
        (b'\xc3\x83\xc2\xa2\xc3\x85\xe2\x80\x9c...', b'\xe2\x9c\x93'),
        (b'\xc3\x83\xc2\xa2\xc3\x85\xe2\x80\x9c', b'\xe2\x9c\x93'),
        
        # ✓ another variant (Sent to DocuSign)
        (b'\xc3\x83\xc2\xa2\xc3\x85\xc2\x9c', b'\xe2\x9c\x93'),
        (b'\xc3\x82\xc2\xa2\xc3\x85\xc2\x9c', b'\xe2\x9c\x93'),
        
        # – en-dash / em-dash
        (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d', b'\xe2\x80\x93'),   # –
        (b'\xc3\xa2\xe2\x82\xac\xc2\x93', b'\xe2\x80\x93'),        # – variant
        
        # → in cloudflare comment  
        (b'\xc3\x83\xc2\xa2\xe2\x80\xa0\xc2\x92', b'\xe2\x86\x92'),
        
        # Admin.js banner chars: â* (decorators in comments)
        (b'\xc3\xa2*', b'*'),
        (b'\xc3\xa2\xe2\x80\x9c\xe2\x80\x94', b'\xe2\x94\x80'),   # ─ box drawing
        (b'\xc3\xa2\xe2\x80\x9c\xc2\x80', b'\xe2\x94\x80'),        # ─ variant

        # Cloudflare guide arrow
        (b'\xc3\x83\xc2\xa2\xe2\x80\xa0\xc2\x92', b'\xe2\x86\x92'),
    ]
    
    for old, new in replacements:
        count = content.count(old)
        if count:
            print(f"  {filepath}: Replacing {count}x {repr(old[:6])}... -> {repr(new)}")
            content = content.replace(old, new)
    
    with open(filepath, 'wb') as f:
        f.write(content)
    print(f"  {filepath}: Done ({original_len} -> {len(content)} bytes)")


fix_file('index.js')
fix_file('admin/admin.js', is_admin=True)
print("All done!")
