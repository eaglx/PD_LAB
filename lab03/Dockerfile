FROM python:3.6

# Add files with data
ADD unique_tracks.txt .
ADD triplets_sample_20p.txt .

# Add script
ADD lab.py .

# Set action on start container
ENTRYPOINT python3 lab.py
