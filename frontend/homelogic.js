const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "/index.html"; // not logged in, redirect back
}
document.getElementById("greeting").textContent = "Welcome, " + token + "!";