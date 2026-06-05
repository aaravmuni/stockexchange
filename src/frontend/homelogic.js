const token = sessionStorage.getItem("token");
if (!token) {
  window.location.href = "/index.html"; 
}
else{
let username = null;

async function loadUser()
{
  const response = await fetch("/me",
  {
    method: "GET",
    headers: {"Authorization": "Bearer "+token}
  });

  if(response.status === 401)
  {
    sessionStorage.removeItem("token");
    window.location.href = "/index.html"; 
    return;
  }

  const data = await response.json();
  username = data["username"];
  greeting.textContent = "Welcom "+username+"!!";
}

const greeting = document.getElementById("greeting");
greeting.textContent = "LOADING..."
loadUser();
}