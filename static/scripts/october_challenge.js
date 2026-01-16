// Replace with your actual Spreadsheet ID
const spreadsheetId = "10MInn7b6-cKpu_e94-99y7YMOw7iI9gx8GQBI_sG2_s";

// Replace with your API Key
const apiKey = "AIzaSyCOyCg5u_dyqHFJa6uQ0nodqRQ3rcFBsWE";

const HELEN_FORM_ID = "";
const MAX_FORM_ID = "";
const BETH_FORM_ID = "";

// Construct the URL for Google Sheets API v4
const url = `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/Sheet1?key=${apiKey}`;


// global variable for data
var global_rows;


// Column key
// 0 - Task
// 1 - Helen
// 2 - Max
// 3 - Beth

var nameMap = {
    "Helen": 1,
    "Max": 2,
    "Beth": 3
}


function onDropDownUpdate() {
    const selectBox = document.querySelector("#nameSelect");
    var value = selectBox.value;
    selected = selectBox.options[selectBox.selectedIndex].text;
    updateTasks(global_rows, selected)
};

function onCheckBoxCompletion() {

};

async function fetchGoogleSheetData() {
    try {
        // Fetch data from Google Sheets API
        const response = await fetch(url);
        const data = await response.json();

        // Extract rows from the data
        const rows = data.values;
        global_rows = rows;

        renderTasks(rows)

    } catch (error) {
        console.error("Error fetching Google Sheets data:", error);
    }
}

function updateTasks(rows, selected) {

    // Loop through each cell in the row and create a table cell for each
    var checkedValue;
    // Loop through the rows (starting from row 1 to skip headers)
    for (let i = 1; i < rows.length; i++) {


        const taskInput = document.querySelector("#task" + i);

        if (selected != "") {
            console.log(selected)
            checkedValue = rows[i][nameMap[selected]];
            console.log("checked value:" + checkedValue)
            if (checkedValue == "Done") {
                taskInput.checked = true;
            } else {

                taskInput.checked = false;
            }
        } else {
            taskInput.checked = false;
        }

    };

}

function renderTasks(rows) {
    // Get the table body element
    const parent = document.querySelector("#task-parent");
    const taskHeader = document.querySelector("#task-header");
    const taskContainer = document.querySelector("#task-container");


    var nameOptions = ["", "Helen", "Max", "Beth"];

    var selectLabel = document.createElement("label");
    selectLabel.setAttribute("for", "nameSelect");
    selectLabel.innerHTML = "Select your name to see your progress:";
    parent.insertBefore(selectLabel, taskHeader);

    //Create and append select list
    var selectList = document.createElement("select");
    selectList.id = "nameSelect";
    selectList.setAttribute("onClick", "onDropDownUpdate()")
    parent.insertBefore(selectList, selectLabel.nextSibling);

    //Create and append the options
    for (var i = 0; i < nameOptions.length; i++) {
        var option = document.createElement("option");
        option.value = nameOptions[i];
        option.text = nameOptions[i];
        selectList.appendChild(option);
    }

    const initial_selected = ""
    // Loop through the rows (starting from row 1 to skip headers)
    for (let i = 1; i < rows.length; i++) {

        var row = rows[i]
        // create an input per row
        var input = document.createElement("input");
        input.setAttribute("type", "checkbox");
        input.setAttribute("id", "task" + i);

        var checkboxLabel = document.createElement("label");
        var checkboxSpan = document.createElement("span");
        checkboxSpan.innerHTML = row[0];
        checkboxLabel.appendChild(input);
        checkboxLabel.appendChild(checkboxSpan);

        // Loop through each cell in the row and create a table cell for each
        var checkedValue;
        //rows[i].forEach((cell, j) => {
        if (initial_selected != "") {
            console.log(initial_selected)
            checkedValue = row[nameMap[initial_selected]];
            console.log("checked value:" + checkedValue)
            if (checkedValue == "Done") {
                input.checked = true;
            } else {

                input.checked = false;
            }
        } else {
            input.checked = false;
        }

        //});
        taskContainer.appendChild(checkboxLabel);
        taskContainer.appendChild(document.createElement("br"))
    }
}



// Call the function to fetch and display data
document.addEventListener("DOMContentLoaded", fetchGoogleSheetData);
