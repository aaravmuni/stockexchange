const token = localStorage.getItem("token");
console.log(token);
if (!token) {
  window.location.href = "/index.html"; 
}

async function loadUser()
{
  const response = await fetch("http://127.0.0.1:8000/me",
  {
    method: "GET",
    headers: {"Authorization": "Bearer "+token}
  });

  if(response.status === 401)
  {
    localStorage.removeItem("token");
    window.location.href = "/index.html"; 
    return;
  }

  const data = await response.json();
  const username = data["username"];
  greeting.textContent = "Welcom "+username+"!!";
}

const greeting = document.getElementById("greeting");
greeting.textContent = "LOADING..."
loadUser();