<div align="center">
  <h2> Data_Visualization </h2>
  <h5> Data visualization project that created after the 7.10, to show attacking groups locations around the world on Israeli websites and help cyber defence groups to draw different conclusions. Can show the amount of groups/attacks (or other numeral data) from each country, with/without dates for a timeline. The database can be read from a local csv/the cloud/SQL </h5>
</div>

<br />

<div align="center">
  
![Project UI Screenshot][Project-UI]

</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#database-selection">Database Selection</a>
    </li>
    <li>
      <a href="#ui">UI</a>
      <ul>
        <li><a href="#dropdown-lists">Dropdown Lists</a></li>
        <li><a href="#map-interaction">Map Interaction</a></li>
      </ul>
    </li>
    <li>
      <a href="#debug">Debug</a>
    </li>
    <li>
      <a href="#notes">Notes</a>
    </li>
  </ol>
</details>


<!-- DATABASE SELECTION -->
## Database Selection
Right after the program starts running, the user will be asked to choice if to use real-data or debug data (see debug section).
If the user will select to not use the local debug files, he will be asked to choose the database location:
* Drive (cloud)
* MySQL
* Local csv (Attacks.csv & Groups Connections.csv files located at ./DataVisualization/Data/)


<br />

<div align="center">
  
![User Database Location Selection][DB-Selection]

</div>
<br />


<!-- UI -->
## UI
**Change Database**: Edit the used database (local/drive/SQL) directly from the website

> [!NOTE]
> This is only a future feature preparation and still aren't functional (the update button will be disabled)

<br />

<div align="center">
  
![Edit Database Page][Edit-DB]

</div>
<br />

### Dropdown Lists
**Map Style**: Choice the visual style of the world map
* 2D
* 3D

<br />

<div align="center">
  
![3D View of The Map][3D-Map]

</div>
<br />

**Graph Type**: Choice the displayed data view
* Map View
* Bars View

<br />

<div align="center">
  
![Data in Bars View][Bars-View]

</div>
<br />

**Selected Data**: Switch between world map view by date or a single frame summary view
* By Date
* Summarized

> [!NOTE]
> "By Date" option is only available with database that contains numeral data + dates

<br />

### Map Interaction
**Mouse Hover**: Allows to see additional info on each country like: Country Name, Number of Attacks/Groups, Date of Data (if available)

**Mouse Click**: Opens popup with a list of all the attack groups from the selected country

There is additional data that will be printed in the python terminal for debug, like: Selected Country Name, Attack Groups in the country, Other Groups that are Connected to those country groups.

<br />

<div align="center">
  
![Terminal Data Example After a Country Selection][Terminal-Data]

</div>
<br />

Also, if connections database file is available, a connection lines between countries will be added in accordance to the connections of different groups.


<!-- DEBUG -->
## Debug
When choosing to use the debug pre-made attacks data, there will be a choice between 3 types of tables data that the program can deal with:
* Attacks + Dates
* Attacks Only
* Groups Only

> [!NOTE]
> Due to confidentiality, currently even if you choose to use "real-data", the database that will be loaded is a copy of "Attacks + Dates" debug file

<br />

<div align="center">
  
![Debug Data Type Selection][Debug-Data-Type]

</div>
<br />

Also, there is in an option inside the code of "main.py" to run the server in debug mode if needed:

```py
app.run(debug=True)
```

When running the server in debug mode, all changes that will be made in the code will also update in the browser when he will be in focus. Also, there will be error monitoring and more debug features from inside the UI (blue circle in the buttom right).

> [!NOTE]
> This browser debug feature isn't recommended anymore, as it will make the user database selection input to re-appear with every auto-refresh


<!-- NOTES -->
## Notes
> [!NOTE]
> If there will be a future need to show numeral data other than "attacks", a little code change will be required as it searching for now for the title "Attacks"

> [!NOTE]
> Currently the code aren't dealing with SQL injections prevention. This will be solved on future updates


<!-- MARKDOWN LINKS & IMAGES -->
[Project-UI]: Pictures/DataVisualization_UI.png
[DB-Selection]: Pictures/DataVisualization_DatabaseSelection.png
[Debug-Data-Type]: Pictures/DataVisualization_DebugDataTypeSelection.png
[3D-Map]: Pictures/DataVisualization_3D_Style.png
[Bars-View]: Pictures/DataVisualization_Bars_View.png
[Edit-DB]: Pictures/DataVisualization_EditDatabase.png
[Terminal-Data]: Pictures/DataVisualization_SelectionTerminalData.png
