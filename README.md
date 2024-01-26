# Spotify Streaming History Parser

This tool parses your extended streaming history from your all-time Spotify data.

### Usage:
Run:
```bash
main.py "path/to/zip/file.zip"
```

### Getting Your Spotify Data:
1. Visit [Spotify Privacy Settings](https://www.spotify.com/us/account/privacy/).
2. Request "Extended Streaming History" (may take up to 30 days).

### Output:
Data is exported to `output/csv/` and `output/html/`

### Known Bugs
Sometimes an artist/song/album will just be NaN, I have not been able to debug this.

### Example Output (HTML)
![HTML Image](https://i.imgur.com/kgwRqMH.png)

### Example Output (CSV)
![CSV Image](https://i.imgur.com/nfNcVVE.png)
