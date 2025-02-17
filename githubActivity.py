import requests
import pandas as pd
import matplotlib.pyplot as plt

GITHUB_USERNAME = input("Your Username: " ) # use your username
TOKEN = input("Your GitHub Token: ")  # use your token

url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
headers = {"Authorization": f"token {TOKEN}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame([
    {
        "Waktu": event["created_at"],
        "Tipe": event["type"],
        "Repository": event["repo"]["name"],
        "URL Repo": event["repo"]["url"]
    }
    for event in data
])


    print(df)
    

    df["Waktu"] = pd.to_datetime(df["Waktu"])


    df_count = df.groupby(df["Waktu"].dt.date).size()

    
    plt.figure(figsize=(10, 5))
    plt.plot(df_count.index, df_count.values, marker="o", linestyle="-", color="blue")
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Aktivitas")
    plt.title(f"Aktivitas GitHub {GITHUB_USERNAME} per Hari")
    plt.xticks(rotation=45)
    plt.grid()

    plt.show()
else:
    print(f"Gagal mengambil data: {response.status_code} - {response.text}")
