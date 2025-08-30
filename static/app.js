const apiBase = "";  // backend base URL
const ws = new WebSocket(`ws://${window.location.host}/ws/tasks`);

const tasksList = document.getElementById("tasks-list");
const titleInput = document.getElementById("title");
const descInput = document.getElementById("description");
const addBtn = document.getElementById("add-task");

// ---- Helper: update text inside li ----
function updateTaskUI(li, task) {
  li.dataset.id = task.id;
  li.querySelector(".task-text").textContent =
    `ID:${task.id} - ${task.title} - ${task.description} [${task.completed ? "✅" : "❌"}]`;
}

// ---- Helper: create <li> for task ----
function renderTaskItem(task) {
  const li = document.createElement("li");
  li.dataset.id = task.id;

  // text span
  const textSpan = document.createElement("span");
  textSpan.className = "task-text";
  textSpan.textContent =
    `ID:${task.id} - ${task.title} - ${task.description} [${task.completed ? "✅" : "❌"}]`;

  // toggle on click
  textSpan.onclick = async () => {
    const res = await fetch(`${apiBase}/tasks/${task.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: !task.completed }),
    });
    const updatedTask = await res.json();
    task.completed = updatedTask.completed; // sync local
    updateTaskUI(li, updatedTask); // update only text
  };

  // delete button
  const delBtn = document.createElement("button");
  delBtn.textContent = "Delete";
  delBtn.onclick = async () => {
    await fetch(`${apiBase}/tasks/${task.id}`, { method: "DELETE" });
  };

  li.appendChild(textSpan);
  li.appendChild(delBtn);
  return li;
}

// ---- Fetch initial tasks ----
async function fetchTasks() {
  const res = await fetch(`${apiBase}/tasks`);
  const tasks = await res.json();
  tasksList.innerHTML = "";
  tasks.forEach(task => tasksList.appendChild(renderTaskItem(task)));
}

// ---- Add task ----
addBtn.onclick = async () => {
  const task = {
    title: titleInput.value,
    description: descInput.value
  };
  const res = await fetch(`${apiBase}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task)
  });
  const newTask = await res.json();
  titleInput.value = "";
  descInput.value = "";
  tasksList.appendChild(renderTaskItem(newTask));
};

// ---- WebSocket for real-time updates ----
ws.onmessage = event => {
  const message = JSON.parse(event.data);
  const task = message.task;

  if (message.type === "task.created") {
    tasksList.appendChild(renderTaskItem(task));

  } else if (message.type === "task.updated") {
    const li = Array.from(tasksList.children).find(li => li.dataset.id == task.id);
    if (li) updateTaskUI(li, task);

  } else if (message.type === "task.deleted") {
    const li = Array.from(tasksList.children).find(li => li.dataset.id == task.id);
    if (li) tasksList.removeChild(li);
  }
};

// ---- Initial fetch ----
fetchTasks();
