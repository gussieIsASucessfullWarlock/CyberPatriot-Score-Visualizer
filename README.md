# CyberPatriot Score Visualizer

![CyberPatriotImageDiffculty](https://user-images.githubusercontent.com/82612866/213948710-67119820-f4d4-4987-a78b-1ac0274f4e4a.png)

This script scrapes the CyberPatriot scoreboard and returns the data for each team in a specified division and tier. It also has the option to graph the data for a specified team.

<h3>Required Libraries</h3>

<ul>
<li>requests</li>
<li>matplotlib.pyplot</li>
<li>bs4 (BeautifulSoup)</li>
<li>time</li>
<li>tqdm</li>
<li>os</li>
<li>tabulate</li>
<li>pandas</li>
</ul>

<h3>Usage</h3>

<p>1. Run the script, it will prompt for a division and tier. If left blank, it will default to "Open" and "Platinum" respectively.</p>
<p>2. The script will then scrape the scoreboard and return the data for each team in the specified division and tier.</p>
<p>3. The script also includes the option to graph the data for a specified team.</p>

<h3>Quick Start</h3>

```
git clone https://github.com/gussieIsASucessfullWarlock/CyberPatriotScoreCalc.git
```

```
pip install requests && pip install matplotlib && pip install bs4 && pip install tqdm && pip install tabulate && pip install pandas && pip install requests
```

```
python3 run.py
```

<h3>FYIs</h3>
<ul>
<li>It's important to note that the script is scraping data from the scoreboard and the webiste could change its structure/design, leading to an error.</li>
<li>The script will take around 0-20 seconds per team depending on how fast your internet connection is.</li>
</ul>
