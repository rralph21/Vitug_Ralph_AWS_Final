const API_BASE = "https://evlhub2nlb.execute-api.us-east-1.amazonaws.com/dev";
const output = document.getElementById("output");

async function loadItems() {
  const response = await fetch(`${API_BASE}/items`);
  const data = await response.json();
  output.textContent = JSON.stringify(data, null, 2);
}

async function loadItemsByLocation(locationId) {
  const response = await fetch(`${API_BASE}/location/${locationId}`);
  const data = await response.json();
  output.textContent = JSON.stringify(data, null, 2);
}