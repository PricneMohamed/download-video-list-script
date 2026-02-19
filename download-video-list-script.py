import yt_dlp
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn

progress = Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    TextColumn("{task.percentage:>3.0f}%"),
    TransferSpeedColumn(),
    TimeRemainingColumn(),
)

def download_with_progress(url):

    task_id = None

    def progress_hook(d):
        nonlocal task_id

        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)

            if total:
                if task_id is None:
                    task_id = progress.add_task("Downloading", total=total)

                progress.update(task_id, completed=downloaded)

        elif d['status'] == 'finished':
            progress.update(task_id, completed=progress.tasks[0].total)
            print("\nMerging audio & video...")

    ytdlpOption = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "merge_output_format": "mp4",
        "progress_hooks": [progress_hook],
    }

    with progress:
        with yt_dlp.YoutubeDL(ytdlpOption) as yt:
            yt.download([url])


url = input("Enter video URL: ")
download_with_progress(url)
