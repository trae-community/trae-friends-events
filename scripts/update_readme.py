import csv
import datetime
import os

# Configuration
COLORS = {
    'Talk': 'FFD54F',
    'Workshop': 'FFB74D',
    'Meetup': '8C9EFF',
    'Demoday': '4DB6AC',
    'Family Day': 'F06292',
    'Hackathon': '4DD0E1',
    'Tea Talk': '4CAF50',
    'Outdoor Exploration': '795548',
    'Open Mic': 'FFD54F',
}

MONTH_NAMES_EN = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

MONTH_NAMES_ZH = {
    1: '1月', 2: '2月', 3: '3月', 4: '4月', 5: '5月', 6: '6月',
    7: '7月', 8: '8月', 9: '9月', 10: '10月', 11: '11月', 12: '12月'
}

HEADERS_EN = ['Date', 'Event Type', 'City']
HEADERS_ZH = ['举办日期', '活动类型', '城市']

def get_badge(event_type):
    color = COLORS.get(event_type, 'FFD54F')
    # Ensure event_type is URL safe if needed, but for now simple replacement space -> %20 might be enough
    # But shield.io handles spaces usually fine or needs %20. Let's use as is, assuming it worked before.
    # Actually, previous readme used spaces in badge url: badge/Outdoor Exploration-795548
    return f'<img src="https://img.shields.io/badge/{event_type}-{color}?style=flat-square">'

def format_date(date_str):
    # date_str is YYYY-MM-DD
    # output MM.DD
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%m.%d')

def generate_markdown(events, lang='en'):
    # events: list of dicts
    # Sort events by date descending
    events.sort(key=lambda x: x['Date'], reverse=True)
    
    # Group by year
    events_by_year = {}
    for event in events:
        year = int(event['Date'].split('-')[0])
        if year not in events_by_year:
            events_by_year[year] = []
        events_by_year[year].append(event)
        
    years = sorted(events_by_year.keys(), reverse=True)
    if not years:
        return ""
        
    current_year = years[0]
    output = []
    
    output.append('<div align="center">')
    output.append('')
    # Current Year Badge
    output.append(f'<img src="https://img.shields.io/badge/{current_year}-101010?style=for-the-badge&logo=google-calendar&logoColor=00E599" height="28">')
    output.append('<br><br>')
    output.append('')
    
    # Process Current Year
    output.extend(generate_year_content(events_by_year[current_year], lang, is_current_year=True))
    
    output.append('</div>')
    output.append('')
    output.append('<br>')
    output.append('')
    
    # Archive Years
    for year in years[1:]:
        archive_title = f"📂 Click to expand {year} Events (Archive)" if lang == 'en' else f"📂 点击展开 {year} 年活动 (Archive)"
        output.append(f'<details>')
        output.append(f'<summary><b>{archive_title}</b></summary>')
        output.append('<br>')
        output.append('')
        output.append('<div align="center">')
        output.append('')
        output.append(f'<!-- Timeline Header -->')
        output.append(f'<img src="https://img.shields.io/badge/{year}-101010?style=for-the-badge&logo=google-calendar&logoColor=00E599" height="28">')
        output.append('<br><br>')
        output.append('')
        
        output.extend(generate_year_content(events_by_year[year], lang, is_current_year=False))
        
        output.append('</div>')
        output.append('')
        output.append('</details>')
        output.append('')
        output.append('<br>')
        
    return '\n'.join(output)

def generate_year_content(events, lang, is_current_year):
    # Group by month
    events_by_month = {}
    for event in events:
        month = int(event['Date'].split('-')[1])
        if month not in events_by_month:
            events_by_month[month] = []
        events_by_month[month].append(event)
        
    months = sorted(events_by_month.keys(), reverse=True)
    output = []
    
    # Determine which month to open
    # If current year, open the first (latest) month. Others closed.
    # If archive, all closed.
    
    for i, month in enumerate(months):
        month_name = MONTH_NAMES_EN[month] if lang == 'en' else MONTH_NAMES_ZH[month]
        is_open = ' open' if (is_current_year and i == 0) else ''
        
        output.append(f'<details{is_open}><summary><b>{month_name}</b></summary>')
        output.append('')
        
        # Table Header
        headers = HEADERS_EN if lang == 'en' else HEADERS_ZH
        output.append(f'| {headers[0]} | {headers[1]} | {headers[2]} |')
        output.append('| :--- | :--- | :--- |')
        
        for event in events_by_month[month]:
            date_str = format_date(event['Date'])
            badge = get_badge(event['Type'])
            city_val = event['City_EN'] if lang == 'en' else event['City_ZH']
            city = f"TRAE Friends@{city_val}"
            output.append(f'| {date_str} | {badge} | {city} |')
            
        output.append('')
        output.append('</details>')
        
    return output

def update_readme(file_path, lang):
    # Read CSV
    events = []
    with open('data/events.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append(row)
            
    new_content = generate_markdown(events, lang)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_marker = '<!-- TIMELINE_START -->'
    end_marker = '<!-- TIMELINE_END -->'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print(f"Error: Markers not found in {file_path}")
        return
        
    final_content = content[:start_idx + len(start_marker)] + '\n' + new_content + '\n' + content[end_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Updated {file_path}")

if __name__ == '__main__':
    update_readme('README.md', 'en')
    update_readme('README.zh-CN.md', 'zh')
