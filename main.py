import re, json, requests
from datetime import datetime, timezone

SOURCE_URL = "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt"

def fetch_data():
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()
    return response.text

def clean_and_filter(content):
    trimmed = "\n".join(content.splitlines()[12:])
    clean_flag = re.sub(r"^.*? ", "", trimmed, flags=re.MULTILINE)
    clean_isp = re.sub(r" \[.*?\]", "", clean_flag, flags=re.MULTILINE)
    lines = clean_isp.splitlines()
    parsed = [l.split(" ") for l in lines]
    
    filtered = []
    for item in parsed:
        if item[2].lower() != "id":
            continue
        
        response_time = int(item[1].replace("ms", "")) or 1000
        if response_time > 500:
            continue
        
        filtered.append(item[0])
    
    return filtered

def main():
    raw_data = fetch_data()
    filtered = clean_and_filter(raw_data)

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(filtered),
        "data": filtered,
    }

    with open("proxy.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()