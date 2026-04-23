const API = "https://your-backend-url-here"; // replace with your backend URL
let token = localStorage.getItem("token") || null;

const authBox = document.getElementById("auth");
const courseBox = document.getElementById("course");
const lessonBox = document.getElementById("lesson");

function showAuth() {
  authBox.innerHTML = `
    <h2>Login / Signup</h2>
    <input id="email" placeholder="Email"><br><br>
    <input id="password" placeholder="Password" type="password"><br><br>
    <button onclick="signup()">Sign Up</button>
    <button onclick="login()">Login</button>
  `;
}

async function signup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  await fetch(API + "/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  alert("Account created. Now log in.");
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(API + "/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  token = data.token;
  localStorage.setItem("token", token);

  loadCourse();
}

async function loadCourse() {
  authBox.innerHTML = "";
  lessonBox.innerHTML = "";

  const res = await fetch(API + "/lessons/");
  const course = await res.json();

  courseBox.innerHTML = `
    <h2>${course.title}</h2>
    <p>${course.description}</p>
    <button onclick="upgrade()">Upgrade to PRO</button>
    <h3>Lessons</h3>
  `;

  course.lessons.forEach(l => {
    courseBox.innerHTML += `
      <div class="lesson">
        <strong>${l.title}</strong><br>
        <button onclick="openLesson(${l.id})">Open</button>
      </div>
    `;
  });
}

async function openLesson(id) {
  const res = await fetch(API + "/lessons/" + id, {
    headers: { Authorization: token }
  });

  const data = await res.json();

  lessonBox.innerHTML = `
    <h2>Lesson ${id}</h2>
    <pre>${data.content}</pre>
    <button onclick="markComplete(${id})">Mark Complete</button>
  `;
}

async function markComplete(id) {
  await fetch(API + "/progress/" + id, {
    method: "POST",
    headers: { Authorization: token }
  });

  alert("Marked complete");
}

async function upgrade() {
  await fetch(API + "/payments/upgrade", {
    method: "POST",
    headers: { Authorization: token }
  });

  alert("Upgraded to PRO");
}

if (!token) {
  showAuth();
} else {
  loadCourse();
}
