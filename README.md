<div align="center">
  <h2> Data_Visualization </h2>
  <h5> Data visualization for the attacking groups locations around the world. Can show the amount of groups from each country OR the amount of the attacks (or other numeral data) from each country, with dates for a timeline or without </h5>
</div>

<br />

> [!NOTE]
> If there is a need to show numeral data other than "attacks", a little code change will be required as it searching for now for the title "Attacks"

<br />

![Project UI Screenshot][Project-UI]


## UI
**Update Database Page**: Edit the database directly from the website

> [!NOTE]
> This is only a future feature preparation and still aren't functional (the update button will be disabled)

<br />

<h3> Dropdown lists </h3>

**Map Style**: Choice the visual style of the world map
* 2D
* 3D

<br />

**Map Style**: Choice the displayed data view
* Map View
* Bars View

> [!NOTE]
> Refers to the center dropdown list. This text typo needs to be fixed!

<br />

**Selected Data**: Switch between world map view by date or a single frame summary view
* By Date
* Summarized

> [!NOTE]
> "By Date" option is only available with database that contains numeral data + dates


## Debug
The first lines of the code inside "main" are been used for loading debug example data files.

Please **DO NOT** leave this section on debug mode while merging to master, as follow:

```py
# Choice between:
# 'Server Data' (default), 'Groups-Debug', 'Attacks-Debug', 'Attacks(Date)-Debug'
file_data = 'Server Data'
# 'Server Data' (default), 'Debug Data'
connections_data = 'Server Data'
```

<br />

Also, in the last line of "main" there is an option to choice to run the server on debug mode as well.

When running the server in debug mode, all changes that will be made in the code will also update in the browser when he will be in focus. Also, there will be error monitoring and more debug features from inside the UI (blue circle in the buttom right).

```py
app.run(debug=True)
```


<!-- MARKDOWN LINKS & IMAGES -->
[Project-UI]: Pictures/DataVisualization_UI.png
