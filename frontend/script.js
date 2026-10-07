

async function loadEmployees() {
    const response = await fetch("/employees");
    const employees = await response.json();
    const table = document.getElementById("employeeTable");
    table.innerHTML = "";
    employees.forEach(function(employee) {
        const row = `
            <tr>
                <td>${employee.id}</td>
                <td>${employee.name}</td>
                <td>${employee.email}</td>
                <td>${employee.department}</td>
                <td>${employee.salary}</td>
                <td>
                    <button onclick="editEmployee(${employee.id})">
                        Edit
                    </button>
                    <button onclick="deleteEmployee(${employee.id})">
                        Delete
                    </button>
                </td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

async function addEmployee() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const department = document.getElementById("department").value;
    const salary = document.getElementById("salary").value;
    const response = await fetch("/employees", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            email: email,
            department: department,
            salary: salary
        })
    });
    const result = await response.json();
    console.log(result);
    await loadEmployees();
    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("department").value = "";
    document.getElementById("salary").value = "";
}

async function editEmployee(id) {
    const name = prompt("Enter new name:");
    if (name === null) {
        return;
    }
    const email = prompt("Enter new email:");
    if (email === null) {
        return;
    }
    const department = prompt("Enter new department:");
    if (department === null) {
        return;
    }
    const salary = prompt("Enter new salary:");
    if (salary === null) {
        return;
    }
    const response = await fetch(
        `/employees/${id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                department: department,
               salary: salary
            })
        }
    );
    const result = await response.json();
    console.log(result);
    await loadEmployees();
}

async function deleteEmployee(id) {
    const confirmDelete = confirm("Are you sure you want to delete this employee?");
    if (!confirmDelete) {
        return;
    }
    const response = await fetch(
        `/employees/${id}`,
        {
            method: "DELETE"
        }
    );
    const result = await response.json();
    console.log(result);
    await loadEmployees();
}

loadEmployees();