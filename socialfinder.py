import os
import requests
import time
import sys
import shutil
import threading
from datetime import datetime
from colorama import Fore, Style, init

init()

RESULTS_PATH = "resultats.txt"

def loading_animation(message, stop_event):
    i = 0
    symbols = ["|", "/", "-", "\\"]
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {symbols[i % len(symbols)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)

def display_watermark():
    print(Fore.MAGENTA + "\nSocial Finder - Recherche de pseudos sur les réseaux\n" + Style.RESET_ALL)

def check_username(username):
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter / X": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Telegram": f"https://t.me/{username}",
        "Roblox": f"https://www.roblox.com/user.aspx?username={username}",
        "VK": f"https://vk.com/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Replit": f"https://replit.com/@{username}",
        "Keybase": f"https://keybase.io/{username}",
        "Patreon": f"https://www.patreon.com/{username}",
        "Behance": f"https://www.behance.net/{username}",
        "Mastodon": f"https://mastodon.social/@{username}",
        "Kick": f"https://kick.com/{username}",
        "Rumble": f"https://rumble.com/user/{username}",
        "XDA": f"https://forum.xda-developers.com/m/{username}",
        "Guns.LOL": f"https://guns.lol/profile/{username}",
    }

    found, not_found = {}, {}

    for site, url in sites.items():
        stop_event = threading.Event()
        loader_thread = threading.Thread(target=loading_animation, args=(f"Vérification sur {site}", stop_event))
        loader_thread.start()

        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                found[site] = url
            else:
                not_found[site] = "Non trouvé"
        except requests.exceptions.RequestException:
            not_found[site] = "Erreur de connexion"

        stop_event.set()
        loader_thread.join()
        sys.stdout.write("\r" + " " * 80 + "\r")

    return found, not_found

def save_results(username, found, not_found):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(f"\nRecherche pour : {username}\n")
        f.write(f"Date & Heure : {timestamp}\n")
        f.write("="*40 + "\n\n")
        f.write("Comptes trouvés :\n")
        for site, url in found.items():
            f.write(f"  - {site}: {url}\n")
        f.write("\nComptes non trouvés :\n")
        for site, status in not_found.items():
            f.write(f"  - {site}: {status}\n")
    print(Fore.GREEN + f"\nRésultats enregistrés dans {RESULTS_PATH}" + Style.RESET_ALL)

def main():
    display_watermark()
    while True:
        username = input(Fore.YELLOW + "\nEntrez le pseudo à rechercher (ou 'exit' pour quitter) : " + Style.RESET_ALL)
        if username.lower() == "exit":
            print(Fore.CYAN + "\nMerci d'avoir utilisé Social Finder. À bientôt.\n" + Style.RESET_ALL)
            break
        print(Fore.CYAN + f"\nRecherche du pseudo '{username}' en cours...\n" + Style.RESET_ALL)
        found, not_found = check_username(username)
        print(Fore.GREEN + "\nComptes trouvés :" + Style.RESET_ALL)
        for site, url in found.items():
            print(f"  {Fore.BLUE}- {site}: {Fore.WHITE}{url}" + Style.RESET_ALL)
        print(Fore.RED + "\nComptes non trouvés :" + Style.RESET_ALL)
        for site, status in not_found.items():
            print(f"  {Fore.RED}- {site}: {status}" + Style.RESET_ALL)
        save_results(username, found, not_found)

if __name__ == "__main__":
    main()