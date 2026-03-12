async function loadApplications() {

    const table = document.getElementById("appTable");

    table.innerHTML = "Loading...";

    const res = await fetch("http://127.0.0.1:5000/applications");

    const data = await res.json();

    table.innerHTML = "";

    data.forEach(app => {

        const row = `

<tr>

<td>${app.name}</td>
<td>${app.email}</td>
<td>${app.phone}</td>
<td>${app.position}</td>

<td>
<a href="http://127.0.0.1:5000/resume/${app.resume}" target="_blank">
<button class="download">Download</button>
</a>
</td>

<td>
<button class="delete" onclick="deleteApp('${app._id}')">
Delete
</button>
</td>

</tr>
`;

        table.innerHTML += row;

    });

}

async function deleteApp(id) {

    if (!confirm("Delete this application?")) return;

    await fetch(`http://127.0.0.1:5000/delete/${id}`, {
        method: "DELETE"
    });

    alert("Application Deleted");

    loadApplications();

}

loadApplications();