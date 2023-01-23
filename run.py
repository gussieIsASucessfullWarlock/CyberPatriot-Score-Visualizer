import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import os
from tabulate import tabulate
import pandas as pd

def getData():
    dataToRTN = []
    devision = input("What is your division (Open): ")
    if devision == "":
        devision = "Open"
    devision = devision.title()


    tier = input("What is your tier (Platinum): ")
    if tier == "":
        tier = "Platinum"
    tier = tier.title()

    url = "http://scoreboard.uscyberpatriot.org/index.php?division=" + devision + "&tier=" + tier
    response = requests.get(url)
    if response.status_code == 429:
        time_left = int(response.headers["Retry-After"]) + 4
        print("The webserver is thinking, waiting:", time_left, "seconds.", end='\r')
        while time_left >= 0:
            sleep(1)
            print("The webserver is thinking, waiting:", time_left, "seconds.", end='\r')
            time_left = time_left - 1
        print("                                                                                         ", end='\r')
        response = requests.get(url)
    x = response.text
    soup = BeautifulSoup(x, 'html.parser')

    team_numbers = []
    table = soup.find('table', {'class': 'CSSTableGenerator'})
    rows = table.find_all('tr')
    cout = 0
    for row in rows:
        if cout != 0:
            cols = row.find_all('td')
            team_number = cols[1].text  # find the team number in the second column
            team_numbers.append(team_number)
        cout += 1

    print("Got", len(team_numbers), tier + " teams.")

    rank = 1
    with tqdm(total=len(team_numbers)) as pbar:
        for i in team_numbers:
            url = "http://scoreboard.uscyberpatriot.org/team.php?team=" + i
            response = requests.get(url)
            if response.status_code == 429:
                time_left = int(response.headers["Retry-After"]) + 4
                print("The webserver is thinking, waiting:", time_left, "seconds.", end='\r')
                while time_left >= 0:
                    sleep(1)
                    print("The webserver is thinking, waiting:", time_left, "seconds.", end='\r')
                    time_left = time_left - 1
                print("                                                                                         ", end='\r')
                response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            data = []
            table = soup.find_all('table', {'class': 'CSSTableGenerator'})[1]
            rows = table.find_all('tr')

            cout = 0
            for row in rows:
                if cout != 0:
                    cols = row.find_all('td')
                    cols = [col.text for col in cols]
                    data.append({
                        "Image": cols[0],
                        "Time": cols[1],
                        "Found": int(cols[2]),
                        "Remaining": int(cols[3]),
                        "Penalties": int(cols[4]),
                        "Score": int(cols[5])
                    })
                cout += 1
            dataToRTN += [{"teamNumber": i, "teamData": data}]
            if os.name == 'nt':
                os.system("cls")
            else:
                os.system("clear")
            print("Got", len(team_numbers), "platinum teams.")
            try:
                print("Getting platinum team", team_numbers[rank + 1], "data. Rank:", rank, end='\r')
            except:
                print("Got all teams. Cleaning up ...", end='\r')
            pbar.update(1)
            rank += 1
    return dataToRTN

def graph(graphdata, ourTeam):
    c = 0
    Server2019 = []
    Windows10 = []
    Fedora36 = []
    Ubuntu22 = []
    AddedServer2019 = False
    AddedWindows10 = False
    AddedFedora36 = False
    AddedUbuntu22 = False
    AddedYourServer2019 = False
    AddedYourWindows10 = False
    AddedYourFedora36 = False
    AddedYourUbuntu22 = False
    for i in graphdata:
        if ourTeam != graphdata[c]['teamNumber']:
            # Extract the team data
            team_data = graphdata[c]['teamData']
    
            # Initialize empty lists for the x and y values and colors
            x_values = []
            y_values = []
            colors = []
            custom_labels = []
    
            # Iterate through each team data point
            for point in team_data:
                # Aggregate the score
                x_values.append(point['Score'])
                # Append the number of found
                y_values.append(point['Found'])
                # Append the color based on the image
                if point['Image'] == 'Fedora36_cpxv_sf_p':
                    Fedora36 += [point['Found']]
                    custom_labels += ["Fedora36"]
                    colors.append('blue')
                elif point['Image'] == 'Server2019_cpxv_sf_pg':
                    Server2019 += [point['Found']]
                    custom_labels += ["Server2019"]
                    colors.append('red')
                elif point['Image'] == 'Ubuntu22_cpxv_sf_pgsms':
                    Ubuntu22 += [point['Found']]
                    custom_labels += ["Ubuntu22"]
                    colors.append('purple')
                elif point['Image'] == 'Windows10_cpxv_sf_p':
                    Windows10 += [point['Found']]
                    custom_labels += ["Windows10"]
                    colors.append('green')
    
            # Create the scatter plot
            # Create a list of custom labels for the legend
    
            # Create the scatter plot with the x and y values and custom labels
            bout = 0
            for i in x_values:
                if custom_labels[bout] == "Fedora36" and AddedFedora36 ==  False:
                    AddedFedora36 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout], label=custom_labels[bout])
                elif custom_labels[bout] == "Server2019" and AddedServer2019 == False:
                    AddedServer2019 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout], label=custom_labels[bout])
                elif custom_labels[bout] == "Ubuntu22" and AddedUbuntu22 == False:
                    AddedUbuntu22 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout], label=custom_labels[bout])
                elif custom_labels[bout] == "Windows10" and AddedWindows10 == False:
                    AddedWindows10 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout], label=custom_labels[bout])
                else:
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout])
                bout += 1
            # Add a label for the x-axis
            plt.xlabel('Score')
            # Add a label for the y-axis
            plt.ylabel('Found')
            # Add a title
            plt.title(f'Top {len(graphdata)} Teams Comp. Data')
            # Display the plot
            c += 1
        else:
            # Extract the team data
            team_data = graphdata[c]['teamData']
    
            # Initialize empty lists for the x and y values and colors
            x_values = []
            y_values = []
            colors = []
            custom_labels = []
    
            # Iterate through each team data point
            for point in team_data:
                # Aggregate the score
                x_values.append(point['Score'])
                # Append the number of found
                y_values.append(point['Found'])
                # Append the color based on the image
                if point['Image'] == 'Fedora36_cpxv_sf_p':
                    Fedora36 += [point['Found']]
                    custom_labels += ["Fedora36"]
                    colors.append('blue')
                elif point['Image'] == 'Server2019_cpxv_sf_pg':
                    Server2019 += [point['Found']]
                    custom_labels += ["Server2019"]
                    colors.append('red')
                elif point['Image'] == 'Ubuntu22_cpxv_sf_pgsms':
                    Ubuntu22 += [point['Found']]
                    custom_labels += ["Ubuntu22"]
                    colors.append('purple')
                elif point['Image'] == 'Windows10_cpxv_sf_p':
                    Windows10 += [point['Found']]
                    custom_labels += ["Windows10"]
                    colors.append('green')
    
            # Create the scatter plot
            # Create a list of custom labels for the legend
    
            # Create the scatter plot with the x and y values and custom labels
            bout = 0
            for i in x_values:
                if custom_labels[bout] == "Fedora36" and AddedYourFedora36 ==  False:
                    AddedYourFedora36 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout])
                    plt.text(x_values[bout], y_values[bout]+1.5, 'Your Fedora', ha='center', bbox={'facecolor':'white', 'edgecolor':'black', 'pad':5, 'alpha':0.8, 'boxstyle':'round,pad=0.5'})
                elif custom_labels[bout] == "Server2019" and AddedYourServer2019 == False:
                    AddedYourServer2019 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout])
                    plt.text(x_values[bout], y_values[bout]+1.5, 'Your Server', ha='center', bbox={'facecolor':'white', 'edgecolor':'black', 'pad':5, 'alpha':0.8, 'boxstyle':'round,pad=0.5'})
                elif custom_labels[bout] == "Ubuntu22" and AddedYourUbuntu22 == False:
                    AddedYourUbuntu22 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout])
                    plt.text(x_values[bout], y_values[bout]+1.5, 'Your Ubuntu', ha='center', bbox={'facecolor':'white', 'edgecolor':'black', 'pad':5, 'alpha':0.8, 'boxstyle':'round,pad=0.5'})
                elif custom_labels[bout] == "Windows10" and AddedYourWindows10 == False:
                    AddedYourWindows10 = True
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout])
                    plt.text(x_values[bout], y_values[bout]+1.5, 'Your Windows', ha='center', bbox={'facecolor':'white', 'edgecolor':'black', 'pad':5, 'alpha':0.8, 'boxstyle':'round,pad=0.5'})
                else:
                    plt.scatter(x_values[bout], y_values[bout], c=colors[bout])
                bout += 1
            # Add a label for the x-axis
            plt.xlabel('Score')
            # Add a label for the y-axis
            plt.ylabel('Found')
            # Add a title
            plt.title(f'Top {len(graphdata)} Teams Comp. Data')
            # Display the plot
            c += 1
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
    plt.legend()
    plt.gcf().set_size_inches(12, 9)
    plt.savefig('CyberPatriotImageDiffculty.png', dpi=800)
    print("Saved plot as", "\"CyberPatriotImageDiffculty.png\"")

def makeTable(tabledata, ourTeam):
    ferdora = "0"
    ubt = "0"
    win = "0"
    ser = "0"
    rnk = "none"
    tdata = []
    bscout = 0
    for i in tabledata:
        bscout += 1
        if i["teamNumber"] == ourTeam:
            rnk = str(bscout)
        try:
            fedoraScore = i["teamData"][0]["Score"]
        except:
            fedoraScore = 0
        try:
            serverScore = i["teamData"][1]["Score"]
        except:
            serverScore = 0
        try:
            ubuntuScore = i["teamData"][2]["Score"]
        except:
            ubuntuScore = 0
        try:
            winScore = i["teamData"][3]["Score"]
        except:
            winScore = 0
        if i["teamNumber"] == ourTeam:
            ferdora = fedoraScore
            win = winScore
            ser = serverScore
            ubt = ubuntuScore
        tdata += [{"Team": i["teamNumber"], "Fedora": fedoraScore, "Server": serverScore, "Ubuntu": ubuntuScore, "Windows": winScore}]
    df = pd.DataFrame(tdata)
    print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
    title = f"===================== {ourTeam} Team Data Report ====================="
    end = ""
    dnd = 0
    while dnd < len(title):
        end += "="
        dnd += 1
    print("")
    print(title)
    print(f"Your team has {ferdora} on Fedora")
    print(f"Your team has {win} on Windows 10")
    print(f"Your team has {ser} on Server")
    print(f"Your team has {ubt} on Ubuntu")
    print(f"Your team has a rank of {rnk}")
    print(end)

data = getData()

teamNumber = os.system("What is your team number: ")
graph(data, teamNumber)
makeTable(data, teamNumber)
