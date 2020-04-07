# Springer Free Books Downloader
<p>
  <img src="https://img.shields.io/pypi/status/Django.svg"/>
  <img src="https://img.shields.io/badge/contributions-welcome-orange.svg"/>
</p>
<p>
Downloads free books offered by <a href="https://www.springer.com/gp">Springer</a>. It will automatically create a springer-books sub-folder in the directory where the scripts run at. The script will categorize the books according the subject.
</p>

## Download
Download both files:
* ```requirements.txt```
* ```download.py```
```
pip3 install -r requirements.txt
python3 download.py
```

## Usage
```
Usage:
		python3 download.py
		python3 download.py -s <subject-classification>
		python3 download.py <option> -s <subject-classification>

Options:
		--epub		Download ePub versions.
```

<b>N.B.</b> Not specifing a subject-classification will download all avaliable books (<i>around 409 books / ~7.2 GB</i>)
