const balmeter = document.getElementById("currentbalance");

async function getbalance() {
    const response = await fetch("/currentbalance",{
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
  balmeter.textContent = data["message"];
}

async function updt10() {
    const response = await fetch("/increaseby10",{
    method: "POST",
    headers: {"Authorization": "Bearer "+token}
    });

    if(response.status === 401)
    {
      sessionStorage.removeItem("token");
      window.location.href = "/index.html"; 
      return;
    }

    const data = await response.json();
    if(data["message"] != "ok")
    {
        alert("increase failed: " + data["message"]);
    }
    getbalance();
}

document.getElementById("plus10").addEventListener("click", updt10);

getbalance();