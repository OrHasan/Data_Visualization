<div align="center">
  <h2> Data_Visualization </h2>
  <h5> Data visualization tool to display attacks around the world by date and time on Israeli websites, aiding cyber defense groups in the analysis process after the events of 7.10 </h5>
  <h5> Provided clear visual insights into attack patterns and origins, enhancing the ability to draw conclusions and respond effectively </h5>
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
        <li><a href="#change-database-button">'Change Database' Button</a></li>
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
Right after the program starts running, the user will be asked to choose whether to use real data or debug data (see debug section).
If the user selects not to use the local debug files, they will be asked to choose the database location:
* Drive (cloud)
* MySQL
* Local CSV (Attacks.csv & Groups Connections.csv files located at ./DataVisualization/Data/)


<br />

<div align="center">
  
![User Database Location Selection][DB-Selection]

</div>
<br />


<!-- UI -->
## UI
### Dropdown Lists
**Map Style**: Choose the visual style of the world map
* 2D
* 3D

<br />

<div align="center">
  
![3D View of The Map][3D-Map]

</div>
<br />

**Graph Type**: Choose the displayed data view
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
> The "By Date" option is only available with databases that contain numeral data + dates

<br />

### Map Interaction
**Mouse Hover**: Allows seeing additional info on each country like:
* Country Name
* Number of Attacks/Groups
* Date of Data (if available)

**Mouse Click**: Opens popup with a list of all the attack groups from the selected country

Additional data will be printed in the python terminal for debugging, such as:
* Selected Country Name
* Attack Groups in the country
* Other Groups that are Connected to those country groups

<br />

<div align="center">
  
![Terminal Data Example After a Country Selection][Terminal-Data]

</div>
<br />

If the connections database file is available, connection lines between countries will be added according to the connections of different groups.


### 'Change Database' Button
Edit the used database (local/drive/SQL) directly from the website

> [!NOTE]
> This is only a future feature preparation and is not yet functional (the update button will be disabled)

<br />

<div align="center">
  
![Edit Database Page][Edit-DB]

</div>
<br />


<!-- DEBUG -->
## Debug
When choosing to use the debug pre-made attacks data, there will be a choice between three types of table data that the program can handle:
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

Also, there is an option inside the code of "main.py" to run the server in debug mode if needed:

```py
app.run(debug=True)
```

When running the server in debug mode, all changes made in the code will also update in the browser when it is in focus. Additionally, there will be error monitoring and more debug features from inside the UI (blue circle in the buttom right).

> [!NOTE]
> This browser debug feature is not recommended anymore, as it will make the user database selection input reappear with every auto-refresh


<!-- NOTES -->
## Notes
> [!NOTE]
> If there is a future need to show numerical data other than "attacks", a small code change will be required as it currently searches for the title "Attacks"

> [!NOTE]
> Currently, the code does not handle SQL injections prevention. This will be addressed in future updates


<!-- MARKDOWN LINKS & IMAGES -->
[Project-UI]: Pictures/DataVisualization_UI.png
[DB-Selection]: Pictures/DataVisualization_DatabaseSelection.png
[Debug-Data-Type]: Pictures/DataVisualization_DebugDataTypeSelection.png
[3D-Map]: Pictures/DataVisualization_3D_Style.png
[Bars-View]: Pictures/DataVisualization_Bars_View.png
[Edit-DB]: Pictures/DataVisualization_EditDatabase.png
[Terminal-Data]: Pictures/DataVisualization_SelectionTerminalData.png
