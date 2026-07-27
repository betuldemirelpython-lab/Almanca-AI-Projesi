import re

html = open('index.html', encoding='utf-8').read()

# 1. Check all section IDs
section_ids = re.findall(r'<section[^>]+id="([^"]+)"', html)
print('SECTION IDs:', section_ids)

# 2. Check all data-tab values on buttons
data_tabs = re.findall(r'data-tab="([^"]+)"', html)
print('DATA-TABs:', data_tabs)

# 3. Check onclick on tab buttons
import re
btn_blocks = re.findall(r'<button[^>]*tab-btn[^>]*>(.*?)</button>', html, re.DOTALL)
print('TAB BUTTONS found:', len(btn_blocks))

# Find onclick in tab buttons
tab_btn_html = re.findall(r'<button[^>]*tab-btn[^>]*>', html)
for b in tab_btn_html:
    print('BTN:', b[:150])

# 4. switchTab definition
if 'function switchTab' in html:
    idx = html.index('function switchTab')
    print('\nswitchTab defined at char:', idx)
    print('CODE:', html[idx:idx+250])
else:
    print('ERROR: switchTab NOT FOUND in HTML!')

# 5. Check tab-content sections
sections = re.findall(r'<section[^>]+class="([^"]*)"[^>]*>', html)
print('\nSECTION classes:', sections)
