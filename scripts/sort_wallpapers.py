
import json
from pathlib import Path

# Lokasi file JSON wallpaper
JSON_FILE = Path("wallpaper.json")


def load_wallpapers():
    """Membaca data wallpaper dari JSON."""
    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"File {JSON_FILE} tidak ditemukan!"
        )

    with JSON_FILE.open("r", encoding="utf-8") as file:
        wallpapers = json.load(file)

    if not isinstance(wallpapers, list):
        raise ValueError(
            "Format wallpaper.json harus berupa array JSON."
        )

    for index, wallpaper in enumerate(wallpapers):
        if not isinstance(wallpaper, dict):
            raise ValueError(
                f"Data wallpaper pada indeks {index} tidak valid."
            )

        if "url" not in wallpaper:
            raise ValueError(
                f"Wallpaper pada indeks {index} tidak memiliki URL."
            )

    return wallpapers


def assign_ids(wallpapers):
    """
    Membuat ID otomatis untuk wallpaper yang belum memilikinya.

    Jika semua wallpaper belum memiliki ID, ID diberikan
    berdasarkan urutan saat ini agar urutannya tidak berubah
    pada proses pertama.

    Wallpaper baru yang ditambahkan kemudian akan mendapat
    ID lebih besar daripada ID yang sudah ada.
    """
    if not wallpapers:
        return

    existing_ids = []

    for wallpaper in wallpapers:
        wallpaper_id = wallpaper.get("id")

        if wallpaper_id is not None:
            if (
                isinstance(wallpaper_id, bool)
                or not isinstance(wallpaper_id, int)
                or wallpaper_id < 1
            ):
                raise ValueError(
                    f"ID wallpaper harus berupa bilangan bulat positif: "
                    f"{wallpaper_id!r}"
                )

            existing_ids.append(wallpaper_id)

    if len(existing_ids) != len(set(existing_ids)):
        raise ValueError(
            "Ditemukan ID duplikat. Setiap wallpaper harus "
            "memiliki ID yang unik."
        )

    # Pertama kali dijalankan: semua wallpaper belum punya ID.
    if not existing_ids:
        total = len(wallpapers)

        for index, wallpaper in enumerate(wallpapers):
            wallpaper["id"] = total - index

        return

    # Wallpaper baru yang belum memiliki ID mendapat nomor
    # di atas ID terbesar yang sudah digunakan.
    next_id = max(existing_ids) + 1

    for wallpaper in wallpapers:
        if "id" not in wallpaper:
            wallpaper["id"] = next_id
            next_id += 1


def sort_wallpapers(wallpapers):
    """Mengurutkan ID terbesar ke terkecil."""
    wallpapers.sort(
        key=lambda wallpaper: wallpaper["id"],
        reverse=True
    )

    return wallpapers


def save_wallpapers(wallpapers):
    """Menyimpan hasil pengurutan ke wallpaper.json."""
    with JSON_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            wallpapers,
            file,
            indent=2,
            ensure_ascii=False
        )
        file.write("\n")


def main():
    wallpapers = load_wallpapers()

    assign_ids(wallpapers)
    sort_wallpapers(wallpapers)
    save_wallpapers(wallpapers)

    print("Berhasil mengurutkan wallpaper!")
    print(f"Jumlah wallpaper: {len(wallpapers)}")

    for wallpaper in wallpapers:
        print(
            f"ID: {wallpaper['id']} | "
            f"Nama: {wallpaper.get('name', 'Tanpa nama')}"
        )


if __name__ == "__main__":
    main()
