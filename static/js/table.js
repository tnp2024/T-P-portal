// Function to fetch student data from Django backend
function fetchStudents() {
    fetch('/api/students/') // Change the URL to match your Django endpoint
        .then(response => response.json())
        .then(data => {
            students = data; // Assuming your Django endpoint returns an array of student objects
            populateTable();
            populateDepartmentFilter(); // Call to populate the department filter dropdown
        })
        .catch(error => {
            console.error('Error fetching student data:', error);
        });
}


// Function to populate the table with student data
function populateTable() {
    var tableBody = document.querySelector("#studentTable table");
    tableBody.innerHTML = '';

    students.forEach(function (student) {
        var row = document.createElement("tr");
        Object.values(student).forEach(function (value) {
            var cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });
        tableBody.appendChild(row);
    });
}

// Filter the table based on input value and criteria
function filterTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("filterInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("studentTable");
    tr = table.getElementsByTagName("tr");

    var criteria = document.getElementById("criteria").value;

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");
        if (td) {
            if (criteria === "" || criteria === "department") {
                txtValue = td[td.length - 1].textContent || td[td.length - 1].innerText;
            } else {
                txtValue = td[Object.keys(td)[td.length - 2]].textContent || td[Object.keys(td)[td.length - 2]].innerText;
            }
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// Initial population of the table
fetchStudents();

// Function to populate the department filter dropdown
function populateDepartmentFilter() {
    var departmentFilter = document.getElementById("departmentFilter");
    var departments = new Set(students.map(student => student.department));
    departments.forEach(department => {
        var option = document.createElement("option");
        option.text = department;
        option.value = department;
        departmentFilter.add(option);
    });
}

// Function to filter the table by department
function filterTableByDepartment() {
    var departmentFilter = document.getElementById("departmentFilter");
    var selectedDepartment = departmentFilter.value.toUpperCase();
    var table = document.getElementById("studentTable");
    var tr = table.getElementsByTagName("tr");

    for (var i = 0; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td")[tr[i].getElementsByTagName("td").length - 18]; // Assuming department is the last column
        if (td) {
            var txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(selectedDepartment) > -1 || selectedDepartment === "") {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}