<div align="center">
  <h3> Data_Visualization </h3>
  Data visualization for the attacking groups locations around the world. Can show the amount of groups from each country OR the amount of the attacks (or other numeral data) from each country, with dates for a timeline or without
</div>

<br />

![Project UI Screenshot][Project-UI]


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
